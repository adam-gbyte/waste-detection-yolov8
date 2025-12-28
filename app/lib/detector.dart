import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:tflite_flutter/tflite_flutter.dart';

class Detector {
  late Interpreter interpreter;
  late List<String> labels;

  Future<void> load() async {
    interpreter = await Interpreter.fromAsset('assets/model/best_float16.tflite');
    final raw = await rootBundle.loadString('assets/model/labels.txt');
    labels = raw.trim().split('\n');
  }

  List<List<double>> run(Float32List input) {
    final output = List.generate(1, (_) => List.generate(8400, (_) => List.filled(8, 0.0)));
    interpreter.run(input.reshape([1, 640, 640, 3]), output);
    return output[0];
  }
}
