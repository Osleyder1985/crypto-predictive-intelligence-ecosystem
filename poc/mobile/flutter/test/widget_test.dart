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

  testWidgets('mobile POC exposes partial and unavailable states', (tester) async {
    await tester.pumpWidget(const CpieMobileApp());
    await tester.pumpAndSettle();
    await tester.tap(find.text('Datos parciales'));
    await tester.pumpAndSettle();
    expect(find.text('Calidad: PARTIAL'), findsOneWidget);
    await tester.tap(find.text('No disponible'));
    await tester.pumpAndSettle();
    expect(find.textContaining('Estructura técnica: NOT_AVAILABLE'), findsOneWidget);
  });

  testWidgets('local retry does not change the simulated environment', (tester) async {
    await tester.pumpWidget(const CpieMobileApp());
    await tester.pumpAndSettle();
    await tester.tap(find.text('Error recuperable'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Reintentar localmente'));
    await tester.pumpAndSettle();
    expect(find.textContaining('Reintento local completado'), findsOneWidget);
    expect(find.textContaining('DEMO — DATOS SINTÉTICOS'), findsOneWidget);
  });
}
