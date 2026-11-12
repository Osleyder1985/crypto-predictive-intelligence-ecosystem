import 'package:flutter_test/flutter_test.dart';
import 'package:cpie_mobile_flutter_poc/main.dart';

void main() {
  testWidgets('mobile POC launches with synthetic disclosure', (tester) async {
    await tester.pumpWidget(const CpieMobileApp());
    await tester.pumpAndSettle();
    expect(find.textContaining('CPIE · MOBILE POC'), findsOneWidget);
    expect(find.textContaining('DEMO — DATOS SINTÉTICOS'), findsOneWidget);
    expect(find.text('Sin datos reales, API, autenticación, persistencia ni trading.'), findsOneWidget);
  });
}
