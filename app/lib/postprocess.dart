class Detection {
  final double x, y, w, h, score;
  final int cls;
  Detection(this.x, this.y, this.w, this.h, this.score, this.cls);
}

List<Detection> decode(List<List<double>> output, double thresh) {
  final results = <Detection>[];

  for (final row in output) {
    final obj = row[4];
    if (obj < thresh) continue;

    int bestCls = 0;
    double bestScore = 0;

    for (int i = 5; i < row.length; i++) {
      if (row[i] > bestScore) {
        bestScore = row[i];
        bestCls = i - 5;
      }
    }

    final score = obj * bestScore;
    if (score > thresh) {
      results.add(Detection(row[0], row[1], row[2], row[3], score, bestCls));
    }
  }
  return results;
}
