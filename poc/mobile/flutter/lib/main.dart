import 'dart:convert';

import 'package:flutter/widgets.dart';
import 'package:flutter/services.dart';
import 'package:schema_engine/schema_engine.dart';

void main() {
  runApp(const CpieMobileApp());
}

class CpieMobileApp extends StatelessWidget {
  const CpieMobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    return WidgetsApp(
      color: const Color(0xFF17365D),
      debugShowCheckedModeBanner: false,
      builder: (context, child) => child ?? const SizedBox.shrink(),
      home: const DemoHome(),
    );
  }
}

class DemoHome extends StatefulWidget {
  const DemoHome({super.key});

  @override
  State<DemoHome> createState() => _DemoHomeState();
}

class _DemoHomeState extends State<DemoHome> {
  late final Future<Map<String, dynamic>> _fixture = _loadFixture();
  String _scenario = 'overview';
  bool _retried = false;
  bool _saved = false;
  String _start = '2025-01-01';
  String _end = '2025-01-07';

  Future<Map<String, dynamic>> _loadFixture() async {
    final raw = await rootBundle.loadString('assets/fixtures/research-demo.json');
    final schemaRaw = await rootBundle.loadString('assets/fixtures/research-demo.schema.json');
    final validator = JsonSchema.parse(schemaRaw).compile();
    final decoded = jsonDecode(raw);
    if (!validator.isValid(decoded)) {
      throw const FormatException('Shared POC fixture failed Draft 2020-12 schema validation.');
    }
    final data = decoded as Map<String, dynamic>;
    if (data['environmentStatus'] != 'SIMULATED' ||
        (data['scenarios'] as List).length != 7 ||
        (data['evaluations'] as List).length != 2) {
      throw const FormatException('Shared POC fixture invariants failed.');
    }
    return data;
  }

  bool get _validRange {
    final start = DateTime.tryParse(_start);
    final end = DateTime.tryParse(_end);
    return start != null && end != null && !start.isAfter(end);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: _fixture,
      builder: (context, snapshot) {
        if (snapshot.hasError) {
          return const _PageShell(
            children: [Text('Fixture load/validation failed.', style: TextStyle(color: Color(0xFFAA2222)))],
          );
        }
        if (!snapshot.hasData) {
          return const _PageShell(children: [Text('Loading synthetic fixture…')]);
        }
        final data = snapshot.data!;
        final scenarios = (data['scenarios'] as List).cast<Map<String, dynamic>>();
        final selected = scenarios.firstWhere((item) => item['id'] == _scenario);
        return _PageShell(
          children: [
            const Text('CPIE · MOBILE POC', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w800, letterSpacing: 1.5, color: Color(0xFF53657B))),
            _Panel(
              color: const Color(0xFFFFF0CC),
              child: Text('${data['disclosure']} · ${data['environmentStatus']}', style: const TextStyle(color: Color(0xFF694900), fontWeight: FontWeight.w800)),
            ),
            const Text('Scenarios', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final entry in const {
                  'overview': 'Resumen',
                  'research-valid': 'Investigación',
                  'research-invalid-range': 'Rango inválido',
                  'partial-data': 'Datos parciales',
                  'not-available': 'No disponible',
                  'recoverable-error': 'Error recuperable',
                  'evaluation-comparison': 'Comparar',
                }.entries)
                  _Action(
                    label: entry.value,
                    selected: _scenario == entry.key,
                    onTap: () => setState(() { _scenario = entry.key; _retried = false; if (entry.key == 'research-invalid-range') { _start = '2025-01-07'; _end = '2025-01-01'; } }),
                  ),
              ],
            ),
            ..._scenarioContent(data),
            _Panel(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Estado esperado: ${selected['expectedState']}', style: const TextStyle(fontWeight: FontWeight.w800)),
                  Text('${selected['expectedOutcome']}'),
                ],
              ),
            ),
            const Text('Evaluación local', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
            _Action(label: _saved ? 'Marcada en esta sesión' : 'Marcar evaluación', onTap: () => setState(() => _saved = true)),
            if (_saved)
              const Text('No persistido. El estado se pierde al cerrar la aplicación.', style: TextStyle(color: Color(0xFF8A5A00), fontWeight: FontWeight.w700)),
            const Text('Sin datos reales, API, autenticación, persistencia ni trading.', style: TextStyle(fontSize: 12, color: Color(0xFF64748B))),
          ],
        );
      },
    );
  }

  List<Widget> _scenarioContent(Map<String, dynamic> data) {
    final result = data['researchResult'] as Map<String, dynamic>;
    final sections = (result['sections'] as List).cast<Map<String, dynamic>>();
    switch (_scenario) {
      case 'overview':
        final selection = data['researchSelection'] as Map<String, dynamic>;
        final period = selection['period'] as Map<String, dynamic>;
        return [
          const Text('Bitcoin · DEMO', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
          Text(result['summary'] as String),
          Text('Período: ${period['start']} → ${period['end']}'),
          Text('Incertidumbre: ${(result['uncertainty'] as Map)['status']}'),
        ];
      case 'research-valid':
        final selection = data['researchSelection'] as Map<String, dynamic>;
        final period = selection['period'] as Map<String, dynamic>;
        return [const Text('Investigación simulada', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800)), Text(result['summary'] as String), Text('Rango: ${period['start']} → ${period['end']}')];
      case 'research-invalid-range':
        return [
          const Text('Validación del período', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
          Text('Inicio: $_start'),
          Text('Fin: $_end'),
          _Action(label: 'Invertir rango de fechas', onTap: () => setState(() { final previous = _start; _start = _end; _end = previous; })),
          Text(_validRange ? 'Rango válido' : 'VALIDATION_ERROR: la fecha inicial debe ser anterior o igual a la final.', style: TextStyle(color: _validRange ? const Color(0xFF176B42) : const Color(0xFFAA2222), fontWeight: FontWeight.w700)),
        ];
      case 'partial-data':
        final quality = data['dataQuality'] as Map<String, dynamic>;
        final coverage = quality['coverage'] as Map<String, dynamic>;
        final gaps = (coverage['missingIntervals'] as List).cast<Map<String, dynamic>>();
        return [
          const Text('Calidad: PARTIAL', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
          Text(coverage['description'] as String),
          for (final gap in gaps) Text('Intervalo omitido: ${gap['start']} → ${gap['end']}. ${gap['reason']}'),
          for (final limitation in (quality['limitations'] as List)) Text('• $limitation'),
        ];
      case 'not-available':
        final section = sections.firstWhere((item) => item['id'] == 'technical-structure');
        return [
          Text('Estructura técnica: ${section['status']}', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
          Text(section['reason'] as String),
        ];
      case 'recoverable-error':
        return [
          const Text('ERROR · DEMO_RECOVERABLE', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
          Text(_retried ? 'Reintento local completado; el fixture sigue en modo SIMULATED.' : 'Fallo sintético recuperable para probar el estado de error.'),
          _Action(label: 'Reintentar localmente', onTap: () => setState(() => _retried = true)),
        ];
      case 'evaluation-comparison':
        final evaluations = (data['evaluations'] as List).cast<Map<String, dynamic>>();
        return [
          const Text('Comparación sintética', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
          for (final item in evaluations)
            _Panel(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('${item['id']} · ${item['status']}', style: const TextStyle(fontWeight: FontWeight.w800)),
              Text(item['createdAt'] as String),
              Text(item['summary'] as String),
              Text('Snapshot: ${item['snapshotId']}'),
            ])),
        ];
      default:
        return const [Text('Unknown scenario')];
    }
  }
}

class _PageShell extends StatelessWidget {
  const _PageShell({required this.children});
  final List<Widget> children;

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.ltr,
      child: ColoredBox(
        color: const Color(0xFFF5F7FA),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(18),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              for (final child in children)
                Padding(padding: const EdgeInsets.only(bottom: 14), child: child),
            ]),
          ),
        ),
      ),
    );
  }
}

class _Panel extends StatelessWidget {
  const _Panel({required this.child, this.color = const Color(0xFFFFFFFF)});
  final Widget child;
  final Color color;

  @override
  Widget build(BuildContext context) => DecoratedBox(
    decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(10), border: Border.all(color: const Color(0xFFE0E6ED))),
    child: Padding(padding: const EdgeInsets.all(14), child: child),
  );
}

class _Action extends StatelessWidget {
  const _Action({required this.label, required this.onTap, this.selected = false});
  final String label;
  final VoidCallback onTap;
  final bool selected;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    selected: selected,
    label: label,
    child: GestureDetector(
      onTap: onTap,
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: selected ? const Color(0xFF17365D) : const Color(0xFFFFFFFF),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: selected ? const Color(0xFF17365D) : const Color(0xFFC8D1DC)),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 9, horizontal: 13),
          child: Text(label, style: TextStyle(color: selected ? const Color(0xFFFFFFFF) : const Color(0xFF26384D), fontWeight: FontWeight.w600)),
        ),
      ),
    ),
  );
}

