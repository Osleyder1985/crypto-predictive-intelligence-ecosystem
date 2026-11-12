import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:schema_engine/schema_engine.dart';
import 'package:cpie_mobile_flutter_poc/main.dart';

void main() {
  test('shared fixture validates against the Draft 2020-12 schema', () async {
    final schemaText = await rootBundle.loadString('assets/fixtures/research-demo.schema.json');
    final fixtureText = await rootBundle.loadString('assets/fixtures/research-demo.json');
    final validator = JsonSchema.parse(schemaText).compile();
    final fixture = jsonDecode(fixtureText) as Map<String, dynamic>;
    expect(validator.isValid(fixture), isTrue);
    final invalidFixture = Map<String, dynamic>.from(fixture)..remove('environmentStatus');
    expect(validator.isValid(invalidFixture), isFalse);
  });

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

  testWidgets('invalid date range is rejected', (tester) async {
    await tester.pumpWidget(const CpieMobileApp());
    await tester.pumpAndSettle();
    await tester.tap(find.text('Rango inválido'));
    await tester.pumpAndSettle();
    expect(find.textContaining('VALIDATION_ERROR'), findsOneWidget);
  });

  testWidgets('evaluation comparison displays both synthetic records', (tester) async {
    await tester.pumpWidget(const CpieMobileApp());
    await tester.pumpAndSettle();
    await tester.tap(find.text('Comparar'));
    await tester.pumpAndSettle();
    expect(find.textContaining('demo-evaluation-001'), findsOneWidget);
    expect(find.textContaining('demo-evaluation-002'), findsOneWidget);
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
