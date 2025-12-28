import 'dart:typed_data';
import 'package:image/image.dart' as img;
import 'package:camera/camera.dart';

img.Image convert(CameraImage image) {
  final int width = image.width;
  final int height = image.height;

  final img.Image imgBuffer = img.Image(width, height);

  final planeY = image.planes[0];
  final planeU = image.planes[1];
  final planeV = image.planes[2];

  final bytesY = planeY.bytes;
  final bytesU = planeU.bytes;
  final bytesV = planeV.bytes;

  final int strideY = planeY.bytesPerRow;
  final int strideU = planeU.bytesPerRow;
  final int strideV = planeV.bytesPerRow;

  final int pixelStrideU = planeU.bytesPerPixel!;
  final int pixelStrideV = planeV.bytesPerPixel!;

  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      final int indexY = y * strideY + x;
      final int indexU = (y ~/ 2) * strideU + (x ~/ 2) * pixelStrideU;
      final int indexV = (y ~/ 2) * strideV + (x ~/ 2) * pixelStrideV;

      final int Y = bytesY[indexY];
      final int U = bytesU[indexU];
      final int V = bytesV[indexV];

      int r = (Y + 1.370705 * (V - 128)).round();
      int g = (Y - 0.337633 * (U - 128) - 0.698001 * (V - 128)).round();
      int b = (Y + 1.732446 * (U - 128)).round();

      r = r.clamp(0, 255);
      g = g.clamp(0, 255);
      b = b.clamp(0, 255);

      imgBuffer.setPixel(x, y, img.getColor(r, g, b));
    }
  }

  return imgBuffer;
}

Float32List preprocess(img.Image image) {
  final resized = img.copyResize(image, width: 640, height: 640);
  final input = Float32List(1 * 640 * 640 * 3);
  int i = 0;

  for (int y = 0; y < 640; y++) {
    for (int x = 0; x < 640; x++) {
      final p = resized.getPixel(x, y);
      input[i++] = img.getRed(p) / 255.0;
      input[i++] = img.getGreen(p) / 255.0;
      input[i++] = img.getBlue(p) / 255.0;
    }
  }
  return input;
}
