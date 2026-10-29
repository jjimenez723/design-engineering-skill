// Native macOS background removal (Apple Vision) — no desktop automation, no CapCut chroma key / "Remove BG".
// Same engine as Finder/Preview "Remove Background". macOS 14+.
//
// usage:
//   swift mac_remove_bg.swift <in.png|jpg|heic|dir> <out.png|dir> [--mode foreground|person] [--quality accurate|balanced|fast]
//
//   foreground (default): VNGenerateForegroundInstanceMaskRequest — any salient subject (products, logos, pets, people).
//   person:               VNGeneratePersonSegmentationRequest — people only; steadier frame-to-frame for video.
//
// A directory input processes every image in it (sorted) and writes same-named PNGs with alpha — use this for
// video: extract frames with ffmpeg, run this, then encode HEVC-with-alpha (see mac_remove_bg_video.sh).
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count >= 3 else {
    FileHandle.standardError.write("usage: mac_remove_bg.swift <in> <out> [--mode foreground|person] [--quality accurate|balanced|fast]\n".data(using: .utf8)!)
    exit(2)
}
func opt(_ name: String, _ def: String) -> String {
    if let i = args.firstIndex(of: name), i + 1 < args.count { return args[i + 1] }
    return def
}
let mode = opt("--mode", "foreground"), quality = opt("--quality", "accurate")
let ctx = CIContext(options: [.useSoftwareRenderer: false])
func fail(_ code: Int, _ msg: String) -> NSError { NSError(domain: "bg", code: code, userInfo: [NSLocalizedDescriptionKey: msg]) }

func removeBackground(_ inURL: URL, _ outURL: URL) throws {
    guard let src = CIImage(contentsOf: inURL, options: [.applyOrientationProperty: true]) else { throw fail(1, "cannot read \(inURL.path)") }
    let handler = VNImageRequestHandler(ciImage: src, options: [:])
    var mask: CIImage
    if mode == "person" {
        let req = VNGeneratePersonSegmentationRequest()
        req.qualityLevel = quality == "fast" ? .fast : (quality == "balanced" ? .balanced : .accurate)
        req.outputPixelFormat = kCVPixelFormatType_OneComponent8
        try handler.perform([req])
        guard let obs = req.results?.first else { throw fail(2, "no person found in \(inURL.lastPathComponent)") }
        mask = CIImage(cvPixelBuffer: obs.pixelBuffer)
        mask = mask.transformed(by: CGAffineTransform(scaleX: src.extent.width / mask.extent.width, y: src.extent.height / mask.extent.height))
    } else {
        let req = VNGenerateForegroundInstanceMaskRequest()
        try handler.perform([req])
        guard let obs = req.results?.first else { throw fail(2, "no foreground subject found in \(inURL.lastPathComponent)") }
        let buf = try obs.generateScaledMaskForImage(forInstances: obs.allInstances, from: handler)
        mask = CIImage(cvPixelBuffer: buf)
    }
    let clear = CIImage(color: .clear).cropped(to: src.extent)
    guard let blend = CIFilter(name: "CIBlendWithMask", parameters: [kCIInputImageKey: src, kCIInputBackgroundImageKey: clear, kCIInputMaskImageKey: mask]),
          let out = blend.outputImage,
          let cg = ctx.createCGImage(out, from: src.extent, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!) else { throw fail(3, "composite failed") }
    guard let dest = CGImageDestinationCreateWithURL(outURL as CFURL, UTType.png.identifier as CFString, 1, nil) else { throw fail(4, "cannot write \(outURL.path)") }
    CGImageDestinationAddImage(dest, cg, nil)
    guard CGImageDestinationFinalize(dest) else { throw fail(5, "cannot finalize \(outURL.path)") }
}

let inURL = URL(fileURLWithPath: args[1]), outURL = URL(fileURLWithPath: args[2])
var isDir: ObjCBool = false
_ = FileManager.default.fileExists(atPath: inURL.path, isDirectory: &isDir)
do {
    if isDir.boolValue {
        try FileManager.default.createDirectory(at: outURL, withIntermediateDirectories: true)
        let exts: Set<String> = ["png", "jpg", "jpeg", "heic", "tif", "tiff"]
        let files = try FileManager.default.contentsOfDirectory(atPath: inURL.path).filter { exts.contains(($0 as NSString).pathExtension.lowercased()) }.sorted()
        for (i, f) in files.enumerated() {
            let name = ((f as NSString).deletingPathExtension) + ".png"
            try removeBackground(inURL.appendingPathComponent(f), outURL.appendingPathComponent(name))
            if i % 30 == 0 { print("\(i + 1)/\(files.count)") }
        }
        print("done \(files.count) frames -> \(outURL.path)")
    } else {
        try removeBackground(inURL, outURL); print("done -> \(outURL.path)")
    }
} catch { FileHandle.standardError.write("error: \(error.localizedDescription)\n".data(using: .utf8)!); exit(1) }
