---
title: "RAW — LIDR workshop preparation hub (Notion), full text"
type: source
status: current
date: 2026-09-08
tags: [raw, harness-engineering, lidr]
sources:
  - https://lidr.notion.site/material-workshop-harness-engineering-202609
---

> **What this is.** Verbatim text of the Notion page *"Material de preparación - [Workshop] Harness Engineering"* by LIDR, captured on 2026-09-08 with every toggle expanded. Original language: Spanish. Kept as raw material so nothing is lost; the digested English version is `sources/2026-09-08-lidr-workshop-harness-engineering.md`.
>
> **Embedded media found on the page** (transcripts of the YouTube ones are in this same folder):
> - Vimeo video `vimeo.com/1124271540` (top of page, promo/intro) — not transcribed.
> - Attached video `Presentacion_Alvaro_Workshop_Harness_Engineering.mp4` (section 0) — not transcribed (Notion attachment, no captions).
> - YouTube `rdrtQyGhjYE` — "¿Qué es un Agentic Engineer?" → `yt-rdrtQyGhjYE-agentic-engineer.md`
> - Attached PDF `AI_Engineering_Impact_Report_Faros_AI.pdf` ("The AI Productivity Paradox") — not extracted.
> - YouTube `eca3lWJgRmA` — "Spec-Driven Development: cómo escalar tu productividad con IA y Contexto" → `yt-eca3lWJgRmA-sdd-prompts-settings.md`
> - YouTube `5s-lvoJpMTY` — "How to Use MCP Servers in Cursor" → `yt-5s-lvoJpMTY-mcp-in-cursor.md`
> - YouTube `okYRbetLh7M` — "Programa como un Senior con IA usando Context Engineering" → `yt-okYRbetLh7M-context-engineering.md`
> - YouTube `fCkTax4WfRA` — "Harness Engineering: las 5 áreas clave" → `yt-fCkTax4WfRA-harness-5-areas.md`
> - ~26 images (screenshots of Cursor settings, diagrams "Pilares uso IA", "harness-engineering.png", "ahorrar-tokens.jpg", the "Guía prompt eng" and "10 prompts para devs" graphics, "Anatomía de un/a AI Champion" graphic). Not OCR'd.

---

# Material de preparación - [Workshop] Harness Engineering

Material exclusivo para los asistentes al workshop "De Developer a AI Champion: Harness Engineering para construir flujos agénticos reales"

**Importante:** Añade hi@lidr.co a tu lista de contactos para recibir todas nuestras comunicaciones. Si aún no lo has agendado el evento en tu calendario, haz clic aquí: Google Calendar >> / Outlook Calendar >>. ¡Mantente atento/a y únete a la comunidad de whatsApp!

## ÍNDICE DE CONTENIDOS

0. Presentación
[Curso] Harness Engineering & SDD
1. El mapa completo del AI Champion
2. Los tres pilares del uso efectivo de la IA
3. La receta perfecta del Context Engineering
4. Harness Engineering
5. Ahorro de tokens
6. Encuesta: ¿Cómo verificas lo que genera tu agente antes de mergear?

## 0. Presentación

Si quieres estar al día con contenido diario, novedades y tutoriales sobre adopción de IA en equipos tech, asistentes de código (Claude Code o Cursor), MCPs, agentes o prompt engineering, síguelo en LinkedIn: **Alvaro Moya**, CTO & Founder de LIDR. Y recuerda que todo el contenido en vídeo lo tendrás disponible en nuestro canal de YouTube: suscríbete, dale clic y disfruta.

[video: Presentacion_Alvaro_Workshop_Harness_Engineering.mp4]

## [Curso] Harness Engineering & SDD

Recuerda, para poder ver todas las secciones de contenido debes dar clic en el ícono para desplegar cada sección. (Course index shown as image: 1. Contexto… 2. …La receta perfecta, 3. Spec-Driven Development.)

## 1. El mapa completo del AI Champion 🏆

**¿Sabías que….?** Nos lo encontramos constantemente en los programas que impartimos en empresas: **cada developer hace la guerra por su cuenta.** La empresa reparte licencias y ya está: sin métricas, sin resultados esperados, sin una manera estandarizada de usar la IA en el equipo. **Ser el AI Champion es exactamente lo que resuelve eso y el plus que hace que tu empresa te identifique como esa figura y te ponga al cargo de la adopción, aumentando tu salario (por supuesto 😎).**

### ¿Quién es el AI Champion?

🏆 Este workshop no va (solo) de aprender una técnica más, sino de un rol que las empresas ya están buscando aunque no tenga nombre propio: el **AI Champion**.

Según el framework de OpenAI Academy, un AI Champion es un empleado interno que promueve, apoya y acelera la adopción práctica de IA en una organización. Es el puente entre la estrategia de IA de alto nivel y el trabajo diario de su equipo. No tiene por qué ser un especialista de IT, ni un líder formal: es un peer advocate, alguien cuya credibilidad hace que la adopción de IA se sienta normal, práctica y pegada a problemas reales.

[image: "Anatomía de un/a AI Champion — el puente entre la estrategia de IA y el trabajo diario de tu equipo"]

El framework distingue dos tipos:
- **Leaders:** champions estratégicos, enfocados en gobierno, métricas y alineación cross-funcional a nivel de equipo grande o empresa entera.
- **Activators:** champions de campo, integrados en un equipo concreto, que diseñan flujos prácticos y ayudan a sus compañeros a ganar confianza inmediata.

Sus responsabilidades principales:
- Detectar casos de uso: identificar flujos repetitivos, lentos o inconsistentes que la IA puede optimizar.
- Guiar la implementación: traducir la estrategia de IA en procesos funcionales del día a día.
- Apoyar a sus compañeros: ayudar a superar la fricción y la ansiedad técnica.
- Traducir lo técnico a negocio: explicar conceptos complejos a stakeholders no técnicos.
- Dar feedback a liderazgo: reportar qué herramientas funcionan y dónde se atasca el equipo.

En LIDR lo definimos de forma más concreta para desarrollo de software: **el AI Champion crea la capa agéntica y gobierna la adopción de IA de manera estandarizada y consistente en el equipo.** Es decir, facilita la incorporación de arneses y metodologías como Spec-Driven Development y su mejora continua. Tiene responsabilidades de gobierno de la IA, y debe tener claro el ciclo **medición → feedback → mejora → distribución**, coordinándose con el resto del equipo. Ahora mismo, el Tech Lead suele ser el perfil que cubre este rol.

#### Un rol en auge: Agentic Engineer

Un Agentic Engineer domina la parte técnica: diseña sistemas que los agentes ejecutan. Un AI Champion suma lo que falta para que eso escale en una organización: influencia, liderazgo, gestión del cambio y capacitación del equipo (→ soft skills sobre una base técnica sólida).

[video: YouTube rdrtQyGhjYE]

#### Datos del sector: salarios, demanda y habilidades

Usar IA para programar ya es la norma, no la excepción. Según la encuesta 2025 de Stack Overflow, el 92,6% de los developers usa un asistente de código IA al menos una vez al mes. GitHub Copilot en solitario supera los 4,7 millones de suscriptores de pago (+75% interanual) y está desplegado en el 90% de las Fortune 100.

Y el mercado ya paga más por saber usarla bien. Según datos de Lightcast, los developers con skills de IA cobran alrededor de un 28% más que sus pares sin esas skills, unos 18.000$ más al año en EEUU.

McKinsey encuestó a 4.500 developers en 150 empresas: los equipos que integran bien la IA en su flujo reducen el tiempo en tareas rutinarias un 46%. La palabra clave es *bien*. No es lo mismo "usar IA" que integrarla con un método.

Y aquí el matiz más importante, con un estudio real detrás: METR hizo un ensayo controlado con developers experimentados. Con herramientas de IA, tardaron un 19% más en completar las tareas y aun así, creían haber ido un 20% más rápido. La sensación de velocidad y la velocidad real no son lo mismo sin un sistema que lo verifique.

Ese último punto es la puerta de entrada a por qué importa el gobierno de equipo, no solo la habilidad individual: El informe *The Acceleration Whiplash* (Faros AI, telemetría de 22.000 developers y más de 4.000 equipos, dos años de datos) lo confirma a escala: la productividad individual sí sube (+66% epics completados por developer, +33,7% throughput), pero sin un sistema detrás, el coste se traslada río abajo: bugs por developer +54%, incidentes por PR más que triplicados (+242,7%), tiempo de revisión +441% (5x), y un 31,3% más de PRs que se mergean sin ninguna revisión.

Te lo traducimos: la aceleración individual sin gobierno de equipo no reduce el trabajo, lo redistribuye y en la fase donde nadie está mirando. El informe tiene datos bastante interesantes, te lo comparto: [pdf: AI_Engineering_Impact_Report_Faros_AI.pdf — "The AI Productivity Paradox"]

El hueco que ocupa el AI Champion: no es la persona que usa la IA más rápido, es la que hace que el resto del equipo la use con el mismo criterio.

La oportunidad: ser el AI Champion dentro de tu organización, sin esperar a que la empresa contrate a alguien externo para el puesto. El rol, en la práctica, cubre:
- Configuración del entorno técnico del agente.
- Coaching de gestión del cambio dentro del equipo.
- El ciclo medición → feedback → mejora → distribución (cambio en el código + capacitación formal + comunicación: tutoriales, webinars, etc.)

## 2. Los tres pilares del uso efectivo de la IA

### Metodología TPC

Nuestra metodología de uso efectivo de IA en desarrollo se apoya en 3 pilares fundamentales:
- **Tool** (Copiloto / Agente de programación): no todas las herramientas son iguales, y controlar bien cada parámetro marca la diferencia.
- **Prompt**: dado que a través de nuestras instrucciones es como operamos a los agentes IA, es fundamental hacerlo bien.
- **Contexto**: el pilar más importante a día de hoy para asegurar que lo que genera la IA se alinea con tu forma de programar y con las directrices del proyecto.

[image: Pilares_uso_IA.png]

### Prompts y settings del copiloto/agente de programación IA

En este vídeo nos centraremos en los dos primeros pilares. Aprenderás a: elegir adecuadamente tu copiloto y configurarlo para sacarle todo el partido (MCPs, settings, modelo LLM, memoria, etc.); estructurar prompts usando las mejores prácticas y usar técnicas avanzadas para mejorar la precisión de tus asistentes de código.

[video: YouTube eca3lWJgRmA]

#### ¿Qué copiloto/agente de programación utilizar?

A día de hoy, mi configuración ideal es: **CLI: Claude Code (17 $/mes)** · **IDE: Cursor (20 $/mes)**.

En caso de que no puedas permitirte ambas, te sugiero comenzar solo por Cursor, o Github Copilot o Codex con sus plugins para VS Code/Jetbrains, para tener una experiencia en IDE similar a lo que estás acostumbrado. Una última alternativa sería usar OpenCode, que tiene modelos gratuitos pero también puedes conectar otros comerciales como Codex, ideal si ya tienes una suscripción de ChatGPT. Además, los 4 tienen un CLI, no tan potente como Claude Code, pero similar, con el que puedes empezar a familiarizarte y, una vez dominado, saltes a Claude Code y saques todo el partido a la terminal.

#### ¿Qué modelo utilizar y cuándo? Mejores modelos 2026

Una de las decisiones más relevantes en el uso de agentes de programación es qué modelo usar. Aquí lo importante a día de hoy no es tanto la marca (los modelos comerciales más conocidos como Claude, Codex, Cursor o Gemini están más o menos a la par), como la capacidad de razonamiento. Saber distinguir en qué tareas es imprescindible un razonamiento profundo, nos permite: tener mucha más precisión y efectividad en el desarrollo; ahorrar tokens y consumo.

En la siguiente tabla te muestro un resumen rápido de qué modelo usar para cada tarea en un flujo de desarrollo común, desde discovery de producto hasta resolución de bugs en producción.

- En el caso de Anthropic, la diferenciación entre modelos está clara al tener nombres diferentes: Sonnet como gama media, y Opus como gama superior.
- En el caso de Google, no es dualidad de modelos, es dualidad de niveles dentro del mismo modelo. Usa un sistema integrado de thinking levels: LOW = equivale a Sonnet (rápido, sin razonamiento profundo); HIGH = equivale a Opus (piensa varios minutos, resultados complejos).
- En el caso de Codex de OpenAI, es un único modelo "high" por diseño, no tiene un hermano menor equivalente a Sonnet. Lo más parecido sería usar GPT-5.2 (base) vs Codex, pero no están posicionados así explícitamente.

| Fase del desarrollo | Anthropic | Google | OpenAI | Por qué |
|---|---|---|---|---|
| Discovery → ideas, contexto inicial | Sonnet | Gemini LOW/MED | — | Rápido, sigue instrucciones con precisión, no sobreingeniería |
| PRD / User Stories | Sonnet | Gemini LOW/MED | — | Iteración ágil sobre borradores, corrección de ambigüedades en ciclos cortos |
| Diseño técnico / arquitectura / Specs | Opus | Gemini HIGH | Codex | Entiende la intención sin que se lo expliques todo; razona sobre trade-offs complejos |
| Implementación rutinaria | Sonnet | Gemini LOW/MED | — | Daily driver por defecto: rápido, fiable, 0% error en edición de código |
| Implementación compleja (legacy, refactor, cross-módulo) | Opus | Gemini HIGH | Codex | Contexto amplio, descompone sin perder hilo, trabaja autónomo |
| Review / debugging superficial | Sonnet | Gemini LOW/MED | — | Suficiente para el 80% de los casos |
| Debugging profundo / seguridad | Opus | Gemini HIGH | Codex | Se centra en la parte difícil sin que se lo pidas; Codex lidera en terminal |
| DevOps / CI-CD / terminal | Opus | Gemini HIGH | Codex | Codex es el más fuerte aquí (77,3% Terminal-Bench vs 65,4% Opus) |
| Mantenimiento en producción | Sonnet | Gemini LOW/MED | — | Iteración continua a coste razonable |

**Regla práctica para SDD:** Opus (modelo superior de la gama) planifica y prepara las especificaciones de manera exhaustiva, Sonnet (modelo inferior de la gama) ejecuta las tareas ya atomizadas.

#### Configuración recomendada del agente

Estas recomendaciones sirven para cualquier agente de IA (Github Copilot, Codex, Opencode) o IDE con IA (Windsurf, Antigravity, Cline), aunque en el vídeo se muestre el ejemplo de Cursor. Simplemente la interfaz cambiará según el plugin o IDE, pero las opciones mencionadas están disponibles en cualquiera de los mencionados y muchos otros. Solo busca cada concepto en la documentación si no lo encuentras.

**MCPs más útiles y recomendados**
- Contexto: Atlassian para Jira y Confluence (o alternativo); Context7; Figma (Framelink o el oficial)
- QA: Playwright
- Errores & Seguridad: Sentry; Snyk

Configurar MCPs es muy sencillo, todo se gestiona en un fichero `mcp.json`. Puedes configurarlo a nivel de SO, IDE o proyecto. Luce así:

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp"
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@microsoft/mcp-server-playwright"]
    }
  }
}
```

Los agentes de programación disponen de accesos directos para configurar los servidores MCP, tanto a nivel visual como con comandos en CLI. Aquí te dejo un ejemplo muy básico en Cursor: [video: YouTube 5s-lvoJpMTY]

**Modelos.** Tienes un resumen completo en la sección anterior de cuándo usar uno u otro modelo en función de la tarea. Si necesitas una recomendación concreta a nivel de proveedor, mi recomendación son los modelos de Anthropic. Las últimas versiones de Opus son las mejores para la planificación de la tarea, y la última de Sonnet (4.6 a día de hoy) para ejecución. En cualquier caso, otras alternativas comerciales como Codex (ideal si ya estás pagando la licencia de ChatGPT) o Gemini Pro son totalmente válidas. En Cursor, composer 2 es muy rápido y fiable.

**Otros:** Privacy mode ON · Memories ON. [images: Cursor settings screenshots]

#### Configuración ideal de Claude Code por su creador, Boris Cherny

Hace unas semanas el creador de Claude Code, Boris Cherny, compartió en X su setup con el que consigue una velocidad de desarrollo y calidad a nivel de muy pocas personas en el mundo. Te compartimos aquí la traducción con screenshots para que la puedas poner en práctica fácilmente:

Mi configuración podría ser sorprendentemente básica. Claude Code funciona de maravilla sin hacerle mucho, así que yo personalmente no lo personalizo mucho. No hay una forma correcta de usar Claude Code: lo construimos intencionalmente de una manera que puedas usarlo, personalizarlo y hackearlo como quieras. Cada persona del equipo de Claude Code lo usa de manera muy diferente. Así que, allá vamos.

1. Ejecuto 5 Claudes en paralelo en mi terminal. Numero mis pestañas del 1 al 5 y uso notificaciones del sistema para saber cuándo un Claude necesita entrada. (code.claude.com/docs/en/terminal-config#iterm-2-system-notifications)
2. También ejecuto de 5 a 10 Claudes en claude.ai/code, en paralelo con mis Claudes locales. Mientras codeo en mi terminal, a menudo paso sesiones locales a la web (usando &), o inicio manualmente sesiones en Chrome, y a veces hago --teleport para ir y venir. También inicio algunas sesiones desde mi teléfono (desde la app de Claude para iOS) cada mañana y durante el día, y las reviso más tarde.
3. Uso Opus 4.5 con thinking para todo. Es el mejor modelo de codificación que he usado, y aunque es más grande y lento que Sonnet, como tienes que guiarlo menos y es mejor para usar herramientas, casi siempre es más rápido que usar un modelo más pequeño al final.
4. Nuestro equipo comparte un solo CLAUDE.md para el repositorio de Claude Code. Lo subimos a git, y todo el equipo contribuye varias veces a la semana. Cada vez que vemos que Claude hace algo incorrectamente, lo agregamos al CLAUDE.md, para que Claude sepa no hacerlo la próxima vez. Otros equipos mantienen sus propios CLAUDE.md. Es trabajo de cada equipo mantener el suyo actualizado.
5. Durante la revisión del código, a menudo etiqueto a @.claude en los PR de mis compañeros de trabajo para agregar algo al CLAUDE.md como parte del PR. Usamos la acción de Github de Claude Code (/install-github-action) para esto. Es nuestra versión de Compounding Engineering de @danshipper.
6. La mayoría de las sesiones comienzan en modo Plan (shift+tab dos veces). Si mi objetivo es escribir un Pull Request, usaré el modo Plan, e iré y vendré con Claude hasta que me guste su plan. A partir de ahí, cambio al modo de aceptar ediciones automáticamente y Claude generalmente puede hacerlo en 1-shot. Un buen plan es realmente importante.
7. Uso comandos de slash para cada flujo de trabajo de "bucle interno" que termino haciendo muchas veces al día. Esto me ahorra tener que hacer prompts repetidos, y hace que Claude también pueda usar estos flujos de trabajo. Los comandos se suben a git y viven en .claude/commands/. Por ejemplo, Claude y yo usamos un comando de slash /commit-push-pr docenas de veces todos los días. El comando usa bash en línea para precalcular el estado de git y algunas otras piezas de información para que el comando se ejecute rápidamente y evite el ir y venir con el modelo. (code.claude.com/docs/en/slash-commands#bash-command-execution)
8. Uso algunos subagentes regularmente: code-simplifier simplifica el código después de que Claude termina de trabajar, verify-app tiene instrucciones detalladas para probar Claude Code de principio a fin, y así sucesivamente. Similar a los comandos de slash, pienso en los subagentes como la automatización de los flujos de trabajo más comunes que hago para la mayoría de los PR. (code.claude.com/docs/en/sub-agents)
9. Usamos un PostToolUse hook para formatear el código de Claude. Claude generalmente genera código bien formateado de fábrica, y el hook maneja el último 10% para evitar errores de formato en CI más tarde.
10. No uso --dangerously-skip-permissions. En cambio, uso /permissions para pre-permitir comandos bash comunes que sé que son seguros en mi entorno, para evitar prompts de permisos innecesarios. La mayoría de estos se suben a .claude/settings.json y se comparten con el equipo.
11. Claude Code usa todas mis herramientas por mí. A menudo busca y publica en Slack (a través del servidor MCP), ejecuta consultas de BigQuery para responder preguntas de análisis (usando bq CLI), obtiene registros de errores de Sentry, etc. La configuración de Slack MCP se sube a nuestro .mcp.json y se comparte con el equipo.
12. Para tareas muy largas, haré: un prompt a Claude para que verifique su trabajo con un agente en segundo plano cuando termine; usaré un hook Stop del agente para hacer eso de manera más determinista, o usaré el plugin ralph-wiggum (originalmente soñado por @GeoffreyHuntley). También usaré --permission-mode=dontAsk o --dangerously-skip-permissions en un sandbox para evitar los prompts de permisos para la sesión, para que Claude pueda cocinar sin que yo lo bloquee. (github.com/anthropics/claude-plugins-official → plugins/ralph-wiggum; code.claude.com/docs/en/hooks-guide)
13. Un consejo final: probablemente lo más importante para obtener excelentes resultados de Claude Code: dale a Claude una forma de verificar su trabajo. Si Claude tiene ese ciclo de retroalimentación, duplicará o triplicará la calidad del resultado final. Claude prueba cada cambio que hago en claude.ai/code usando la extensión de Chrome de Claude. Abre un navegador, prueba la interfaz de usuario e itera hasta que el código funcione y la UX se sienta bien. La verificación se ve diferente para cada dominio. Podría ser tan simple como ejecutar un comando bash, o ejecutar un conjunto de pruebas, o probar la aplicación en un navegador o simulador de teléfono. Asegúrate de invertir en hacer esto sólido como una roca.

#### Guía básica de prompt engineering

Aprende a estructurar prompts técnicos y mejorar la precisión de tus asistentes de código: [image: Guia_prompt_eng.jpg]

#### Prompts avanzados

**Meta Prompt**

```
# Instructions
You are an expert in prompt engineering.

Given the following prompt, prepare it using best-practice structure (role, objective, etc.) and formatting to achieve a precise and comprehensive result. Stick strictly to the requested objective by carefully analyzing what is asked in the original prompt.

# Original Prompt:
[Your prompt here, example below]
Provide unit tests for the functionality to retrieve the candidates for a position
```

**Resultado**

```
# ROLE
You are an expert in JavaScript/TypeScript testing specialized in Node.js applications with Express, Prisma ORM, and Jest as the testing framework.

# CONTEXT
You are working on an Applicant Tracking System (ATS) that manages candidates, job positions, and interview processes. The system uses:
- **Backend**: Node.js + Express + TypeScript + Prisma ORM + PostgreSQL
- **Testing**: Jest with mocks
- **Architecture**: Controllers → Services → Database

# OBJECTIVE
Create comprehensive and exhaustive unit tests for the functionality "retrieve candidates for a position," which includes:
1. **Endpoint**: `GET /positions/:id/candidates`
2. **Controller**: `getCandidatesByPosition` in `positionController.ts`
3. **Service**: `getCandidatesByPositionService` in `positionService.ts`

# SPECIFIC REQUIREMENTS
## Functionality to Test
The `getCandidatesByPositionService` function must:
- Receive a `positionId` (number)
- Query `applications` for that position via Prisma
- Include related data: `candidate`, `interviews`, `interviewStep`
- Compute the average of interview scores
- Return an array with: `fullName`, `currentInterviewStep`, `candidateId`, `applicationId`, `averageScore`

## Required Test Cases
### Successful Tests
- ✅ Return candidates with correct averages when data exists
- ✅ Return an empty array when there are no candidates
- ✅ Compute average 0 when there are no interviews
- ✅ Handle multiple candidates with different scores
- ✅ Correctly format `fullName` (firstName + lastName)
### Error Tests
- ❌ Handle database connection errors
- ❌ Handle unexpected Prisma responses
- ❌ Propagate errors with descriptive messages
### Edge Case Tests
- 🔍 Handle `positionId` = 0
- 🔍 Handle negative `positionId`
- 🔍 Handle very large `positionId`
- 🔍 Handle interviews with `null` scores
- 🔍 Handle candidate names with special characters

## Test Structure
describe('getCandidatesByPositionService', () => {
  describe('Successful cases', () => { // Normal functionality tests });
  describe('Error cases', () => { // Error handling tests });
  describe('Edge cases', () => { // Edge case tests });
});

# RESPONSE FORMAT
Provide:
1. **Complete test file** with all necessary imports
2. **Mock setup** for Prisma
3. **Realistic test data** for different scenarios
4. **Specific assertions** that validate both returned data and Prisma calls
5. **Explanatory comments** for complex cases

# QUALITY STANDARDS
- 100% code coverage
- Independent tests (no interdependencies)
- Realistic ATS-domain test data
- Appropriate mocks without side effects
- Detailed and specific assertions
- Explicit handling of async/await
```

**Pregunta al experto**

```
# Role
You are an expert software engineer with experience in modeling architectures and databases.

# Objective
Build a data model for an application with the following functionalities:
- Core value: uses AI to generate personalized company reports for investors. It needs the company website URL and some investor data to personalize (ideal round size, preferred industries, etc.).
- The application allows chatting with AI to extract detailed information from each of the reports. Take into account the data modeling required for ChatGPT-like applications and apply best practices for storing conversations.

# Clarifications about the model:
- Users will register with email and password, and we will have Google SSO.
- Profile data will be basic: name, role in the company (text).
- Users will belong to a company that buys seats for its users—a standard SaaS model. This requires having company information and linking it to its seats, as well as assigning a user role (administrator, analyst), configured by the admin.
- Users will pay with Stripe, with an integration similar to ChatGPT. Store the necessary information for this in a `subscription` table. There is only one price now, but there may be more in the future; create a separate table for pricing.
- Reports will be stored in a `report` table: the submitted website, the company name, the raw report, and the URL of the generated PDF stored in the cloud for download (not all will generate one).
- Chats, as explained, must be stored to maintain history.

Analyze the project and ask me any questions you consider necessary to clarify before proposing the solution.
```

**10 prompts avanzados por caso de uso** [image: 10_prompts_para_devs.jpg]

## 3. La receta perfecta del Context Engineering

### El pilar más importante: el contexto

En este video nos centraremos en el Contexto, el pilar más importante para garantizar respuestas de calidad de tu agente IA en desarrollo: [video: YouTube okYRbetLh7M]

**Especificaciones técnicas**
- Stack tecnológico
- Setup del entorno de desarrollo
- Arquitectura y estructura de ficheros
- Entidades del modelo de datos (enseñar data-model.mdc)
- Patrones de diseño y convenciones: patrones de diseño de APIs, estructura de los tests (mostrar testing-standards.mdc), reglas de nombres, git workflow, clean code / SOLID, patrones, patrones de validación de formularios, manejo de errores, logging, prácticas de ciberseguridad, forma de documentar el código y comentarios
- Aplica tanto a backend como a frontend y mobile (mostrar frontend-standards.mdc)

**Flujo de trabajo**
Desde que hay una petición hasta que el código está funcionando en producción…
- ¿Qué proceso sucede de manera sistemática?
- ¿Quién interviene?
- Cada uno de ellos, ¿qué función tiene en ese proceso? ¿Cuál es su entregable? Una PRD o historia de usuario, un ticket de trabajo técnico, el código como tal, unos tests que validen que el código funciona acorde a las especificaciones, un reporte de tests manuales o automáticos que verifiquen que el código funciona, documentación de lo que se ha hecho…?
- ¿Qué define a cada uno de los entregables para ser considerado excelente?

- Usa ficheros separados para cada elemento y referencia a todos desde un archivo base
- Utiliza git worktrees para cada ticket

**Contexto compartido y actualizado** — De productividad individual a transformación colectiva: Consistencia · Coherencia · Independencia del prompt · Independencia del nivel de seniority

## 4. Harness Engineering

Programar con agentes de IA sin una estructura clara es como soltar a un robot en una cocina sin recetas: el resultado siempre será caótico e impredecible. El Harness Engineering es la disciplina que define las instrucciones, herramientas, entornos locales y bucles de verificación necesarios para que la IA genere código consistente, seguro y listo para producción.

En este video, desglosamos los 5 pilares fundamentales de esta capa agéntica y te mostramos con un ejemplo en vivo cómo pasar de pelear con el prompt a orquestar flujos de desarrollo verdaderamente autónomos: [video: YouTube fCkTax4WfRA]

### Diferencias Context, Harness y Loop Engineering

No son sinónimos. Son niveles de una pirámide. Sin la base, los pisos de arriba no se sostienen.

En la base está el **Context Engineering**. Diseñar qué información ve el agente antes de responder. No solo el prompt, sino todo lo que lo rodea: las convenciones del proyecto, el stack tecnológico, el flujo de trabajo del equipo, las restricciones que no se pueden saltar.

En el nivel intermedio, **Harness Engineering**. No solo preparas la información, construyes el entorno completo en el que el agente opera: herramientas conectadas, checks automáticos, acceso a tus sistemas.

En el vértice, **Loop Engineering**. Ya no activas el agente tú. Diseñas el sistema que lo activa, comprueba los resultados y decide qué viene después. El developer deja de ejecutar tareas para diseñar el sistema que las ejecuta.

Cuanto más arriba en la pirámide, más leverage, pero cada nivel depende del anterior. El Loop construido sobre un contexto desorganizado amplifica los problemas que ya existen. [image: harness-engineering.png]

### La capa que decide si tus agentes llegan a producción

La fórmula ya es canónica en el sector, según Mitchell Hashimoto (cofundador de HashiCorp): **Agent = Model + Harness.**

El modelo pone la inteligencia. El harness es todo lo demás: el contexto que recibe, las reglas que respeta, las herramientas a las que accede, los tests y evals que verifican lo que produce, el sandbox donde ejecuta, y la observabilidad para saber qué decidió y por qué.

Si el modelo es la CPU y el contexto es la RAM, el harness es el sistema operativo. El agente es la aplicación que corre encima. Sin sistema operativo, la CPU más potente del mundo no hace nada útil.

### Por qué el modelo casi nunca es el problema

- Vercel eliminó el 80% de las herramientas de su agente de texto-a-SQL: la tasa de éxito subió del 80% al 100%, con respuestas 3,5 veces más rápidas y un 37% menos de tokens. Mismo modelo, mejor arnés.
- LangChain llevó su agente de programación de la posición 30 a la 5 en el benchmark Terminal-Bench 2.0 — casi 14 puntos de mejora — sin tocar el modelo.
- Stripe mergea 1.300 PRs a la semana sin que un ingeniero escriba código, solo lo revisa.

### Las 5 primitivas de cualquier arnés

- **Filesystem:** almacenamiento durable donde el agente guarda y recupera estado entre pasos.
- **Ejecución de código:** darle al agente una terminal es darle una computadora de propósito general.
- **Sandbox:** ejecución aislada para que el agente actúe sin riesgo de romper producción.
- **Memoria y búsqueda:** aprendizaje continuo tanto de las instrucciones del proyecto, como la búsqueda web y bases de conocimiento vectoriales.
- **Gestión del contexto:** compactación y descarga de información para combatir el context rot.
- **Guías y sensores:** las guías actúan antes de ejecutar (AGENTS.md, linters, restricciones); los sensores actúan después (tests, evals, validación). Un buen harness combina ambos.

[image: harness-engineering2.png]

Artículo completo con la comparativa Harness Engineer vs AI Engineer vs Agentic Engineer vs MLOps Engineer: https://www.lidr.co/blog/que-es-harness-engineering/

### Frameworks para construir tu propio arnés y cuándo usar cada uno

- **OpenSpec:** protocolo de especificación abierto. Ideal para empezar.
- **Spec-Kit (GitHub):** la apuesta de GitHub, bien integrada en su ecosistema.
- **Superpowers:** colección de skills, no specs.
- **Spec-Boot (LIDR):** el más estricto, para equipos y devs que necesitan que el estándar se cumpla siempre.

**¿Por dónde empiezo?** OpenSpec si quieres empezar ya, en un proyecto real, sin montar infraestructura. Spec-Kit si tu organización necesita que quede todo documentado y auditable. Superpowers si lo que te falta no es planificación sino disciplina de ejecución (que el agente no se salte los tests). Y Spec-Boot no es una alternativa a elegir, sino la capa de contexto que pones debajo de cualquiera de los tres para que todos tus copilotos lean las mismas reglas.

### Git Worktrees

Un git worktree es un directorio de trabajo adicional, con su propia carpeta en disco y su propia rama activa, pero que comparte el historial de commits, los objetos de git y la configuración con tu repositorio principal.

En un repo normal, solo puedes tener una rama "activa" a la vez — si Claude Code está a mitad de generar una feature en feature/pagos, tu carpeta de trabajo está en ese estado intermedio, y no puedes cambiar de rama ni abrir otra sesión sobre los mismos ficheros sin pisar ese trabajo.

Un worktree resuelve esto creando una segunda carpeta (../mi-proyecto-pagos/), en una rama distinta, con sus propios ficheros en disco — pero sin duplicar el repositorio. Todo el historial de git se sigue compartiendo.

```bash
git worktree add ../mi-proyecto-pagos feature/pagos   # crear
git worktree list                                     # ver todos
git worktree remove ../mi-proyecto-pagos              # eliminar al terminar
```

**IMPORTANTE:** Sin worktrees, dos sesiones de Claude Code (o Cursor, Codex, etc.) sobre el mismo directorio se pisan: una sobrescribe cambios de la otra, los tests fallan por razones que no tienen que ver con la feature en curso, la base de datos de desarrollo queda en un estado inconsistente.

Con un worktree por sesión, cada agente ve solo sus propios ficheros, corre contra su propia base de datos (si se combina con aislamiento de BBDD) y no tiene ninguna conciencia de que existen otras sesiones. La resolución del problema no es "coordinación inteligente entre agentes" — es aislamiento físico a nivel de sistema de ficheros, que evita que necesiten coordinarse.

Claude Code ya tiene soporte nativo:

```bash
claude --worktree nombre-feature
```

Esto crea el worktree, arranca la sesión dentro, y al salir te pregunta si quieres conservarlo o eliminarlo. También existe `isolation: worktree` para que los subagentes (no solo las sesiones que tú abres) trabajen aislados entre sí — imprescindible si le pides a Claude que reparta un trabajo grande entre varios subagentes en paralelo.

**El "impuesto" de los worktrees.** No son gratis:
- Cada worktree es un checkout nuevo — no arrastra .env, node_modules ni dependencias instaladas. Hay que instalarlas de nuevo en cada uno (o usar un fichero .worktreeinclude para copiar automáticamente lo necesario).
- Si dos worktrees comparten base de datos o puerto de servidor de desarrollo, sigues teniendo colisión — el worktree resuelve el aislamiento de ficheros, no el de infraestructura. Para aislamiento completo, se combina con bases de datos separadas por rama y puertos distintos por sesión.
- Para tareas rápidas (10 minutos), el coste de montar el worktree puede no compensar. La recomendación general es: si normalmente crearías una rama nueva para evitar conflictos, usa un worktree — si no, no merece la pena.

### Los 4 frameworks al detalle

**OpenSpec (Fission-AI)**

Qué es: un framework de SDD ligero, basado en el concepto de *delta specs* — en vez de reescribir toda la especificación cada vez, cada cambio describe solo lo que se añade, modifica o elimina respecto al spec actual:

```
## ADDED Requirements
### Requirement: Autenticación de dos factores
El sistema DEBE soportar 2FA basado en TOTP.
```

Esto es clave para proyectos brownfield (código ya existente, que es el 90% de los casos reales) — no tienes que describir todo el sistema desde cero, solo lo que cambia.

Flujo de trabajo:
```
/opsx:explore → (opcional) pensarlo en voz alta con la IA antes de comprometerte a nada
/opsx:propose → la IA redacta propuesta + specs + diseño técnico + lista de tareas
/opsx:apply   → la IA implementa
/opsx:archive → el delta se fusiona con el spec permanente del proyecto
```

Punto fuerte: fricción mínima. `npm install -g @fission-ai/openspec` + `openspec init` y ya estás trabajando. Sin fases rígidas — puedes actualizar cualquier artefacto en cualquier momento. Compatible con 30+ asistentes de IA. Es, con diferencia, el más popular de los tres (framework, no plugin): ~60.000 estrellas en GitHub.

Punto débil: la función pensada para equipos grandes (Stores, specs compartidas entre varios repos) está en beta muy temprana — "expect breaking changes while it stabilizes", según su propia documentación. Para un individuo o equipo pequeño en un solo repo, no es un problema; para una organización con specs cruzando varios repositorios, todavía es terreno inestable.

**Spec-Kit (GitHub)**

Qué es: el enfoque más estructurado y con más "puertas de calidad" de los tres. En vez de una propuesta → aplicar, tiene fases explícitas con checkpoints:

```
constitution → specify → clarify → plan → tasks → analyze → implement
```

La *constitution* es el documento de reglas no negociables del proyecto (arquitectura, estándares, restricciones de seguridad) — todas las fases posteriores tienen que respetarla. El comando `/analyze` es un control de calidad real: revisa que spec, plan y tareas sean consistentes entre sí antes de dejarte implementar.

Punto fuerte: gobernanza. Tiene extensiones y "presets" para exigir trazabilidad regulatoria, forzar revisiones de seguridad, o adaptar el flujo a metodologías concretas (Agile, Kanban, TDD obligatorio). Es el más indicado si tu organización necesita auditoría o cumplimiento. Además tiene el mayor número de integraciones (30+) y el respaldo de GitHub/Microsoft.

Punto débil — y esto conviene contarlo con honestidad, no solo el marketing oficial: es pesado para tareas pequeñas, y la ejecución de tareas sigue siendo secuencial (no reparte trabajo entre varios agentes en paralelo de forma nativa). En su propio foro de discusión hay opiniones divididas — un usuario lo describe como que "solo complica el trabajo... no se trata de desarrollo de software, sino de generar ideas", mientras otro lo defiende como "un framework para desarrollo sistemático en la era de la IA". Ambas opiniones son reales y conviven en la misma comunidad — depende mucho del tipo de proyecto. También ha tenido cambios de CLI recientes (v0.10 eliminó los flags antiguos --ai), así que tutoriales o vídeos de antes de junio de 2026 pueden mostrar comandos que ya no funcionan.

**Superpowers (obra / Jesse Vincent)**

Qué es: Superpowers no es un framework de specs como los dos anteriores. Es un framework de skills de comportamiento: una librería que se instala como plugin y cambia cómo actúa el agente desde el primer mensaje, sin que tengas que pedirlo cada vez.

En vez de escribir código directamente, el agente:
- Hace preguntas tipo socrático hasta extraer una spec real de la conversación (evita el "el usuario dice 'haz login' y la IA arranca sin saber si es web o móvil, con qué proveedor, etc.")
- Construye un plan de implementación
- Lanza un proceso de desarrollo dirigido por subagentes, aplicando TDD red/green/refactor de verdad, YAGNI y DRY como reglas no opcionales
- Usa git worktrees de forma nativa para que esos subagentes no se pisen entre sí, y al terminar puede fusionar el worktree de vuelta a la rama origen automáticamente

Punto fuerte: disciplina de ingeniería real, forzada, no sugerida. Cero dependencias externas por diseño (no necesita MCPs de terceros para funcionar). Funciona en muchos agentes distintos, no solo Claude Code. Y hay una señal de calidad poco común: el propio repositorio tiene una tasa de rechazo de PRs del 94% — los mantenedores explícitamente rechazan cualquier PR con "invented claims, fabricated problem descriptions, or hallucinated functionality". Es exactamente el tipo de rigor que casa con la voz de LIDR de "evidencia primero".

Punto débil: al no ser un framework de specs, no genera un documento de especificación legible y compartible que el resto del equipo pueda revisar antes de que se escriba código — que es justo el punto fuerte de OpenSpec y Spec-Kit. Es más una herramienta para un developer (o un equipo pequeño) que quiere rigor de ejecución, no un proceso de planificación de equipo grande con revisión humana explícita del plan.

**Spec-Boot (LIDR)**

Spec-Boot no es un motor de specs que compita con los tres anteriores. Su propio README lo deja claro: al instalarlo, explícitamente no instala OpenSpec ni cambia su configuración. Es un kit de reglas, estándares y configuraciones de agente portátil, pensado para complementar a cualquiera de los frameworks anteriores, no sustituirlos.

Qué contiene en concreto: una carpeta docs/ con especificación de API en formato OpenAPI (api-spec.yml), modelo de datos (data-model.md) y guía de desarrollo (development_guide.md) — los mismos ficheros que en la sección 3 del hub ("especificaciones técnicas") decíamos que había que crear. Spec-Boot te da la plantilla ya montada, con symlinks para que cualquier copiloto (Claude, Cursor, Copilot, Codex...) lea el mismo contexto, en vez de tener un fichero de reglas distinto para cada herramienta.

Punto fuerte: es agnóstico de copiloto (un solo set de reglas para todos los agentes que uses) y es gratuito, MIT, mantenido por LIDR.

Punto débil: Es la capa de contexto — hace falta combinarlo con un motor de specs si quieres el flujo completo, no es un sustituto de "elegir un framework".

## 5. Ahorro de tokens

Uno de los beneficios de un harness bien construido: el ahorro de tokens.

La IA, mal utilizada, consume muchísimo con cada petición: revisa el repositorio completo de código en busca de respuestas cada vez, y cada herramienta conectada (skills, MCPs, comandos de terminal) añade tokens a cada llamada.

Las 4 claves que más ahorro dan: [image: ahorrar-tokens.jpg]

5 librerías open source por orden de facilidad de instalación:
1. **rtk:** comprime la salida de terminal antes de que la vea el modelo. 60-90% menos tokens en comandos habituales.
2. **codegraph:** grafo del código 100% local; el agente consulta en vez de explorar archivo a archivo. ~57% menos tokens de media.
3. **caveman:** respuestas del agente sin relleno. ~65% menos tokens de salida.
4. **ponytail:** ataca el código que escribe el agente, no lo que dice. Hasta 80-94% menos código en sobreconstrucción.
5. **Headroom:** comprime contexto (logs, tests) antes de que cuente como input. Hasta 95% según su documentación.

Enlaces: github.com/rtk-ai/rtk · github.com/colbymchenry/codegraph · github.com/JuliusBrussee/caveman · github.com/DietrichGebert/ponytail · github.com/headroomlabs-ai/headroom

En mi propio uso, aplicando esto, he llegado a ahorrar hasta un 60% de tokens. Es mi experiencia, no un benchmark de laboratorio, pero las cifras de cada herramienta sí son públicas y verificables.

Una capa más: routing automático. Cursor, GH Copilot y otros ya traen un modo "Auto" que decide el modelo por tarea. Para más control, OpenRouter o LiteLLM hacen lo mismo a nivel de API.

Tendencia a vigilar: ejecución en modelos locales para tareas bien definidas (Qwen, Kimi, GLM). Este terreno cambia mes a mes, reduciéndose progresivamente la brecha entre los últimos modelos comerciales y open source. Verifica la versión vigente antes de recomendarla a tu equipo.

Artículo completo con las 5 herramientas explicadas a fondo: https://www.lidr.co/blog/como-ahorrar-tokens-en-desarrollo-de-software/

## 6. Encuesta: ¿Cómo verificas lo que genera tu agente antes de mergear?

👀 Si tengo que revisar a mano todo lo que genera un agente, no estoy ganando la eficiencia que promete. Solo estoy moviendo el cuello de botella de «escribir código» a «revisar código».

¿No fue esa la promesa de la IA? ¿Ir más rápido?

Del otro lado, hay quien te diría que confiar al 100% en tests y evals automáticos, sin mirar nada a mano, es directamente temerario, que un test pasa aunque la lógica de negocio esté mal, y que eso te puede explotar en producción sin avisar.

Las dos posturas tienen defensores convencidos. Y probablemente tú no estás en ninguno de los extremos.

¿Cómo verificas lo que genera tu agente antes de mergear? Vota aquí y cuéntame la tuya en comentarios, sobre todo si no está en la lista. (LinkedIn post by Álvaro Moya, urn:li:ugcPost:7502751609286828032: "...Por cierto, construir los sensores correctos es una de las claves de un arnés sólido. Mañana lo cuento en directo... DE DEVELOPER A AI CHAMPION — Aprende Harness Engineering para construir flujos agénticos reales — martes 8 de septiembre, 🇲🇽 10h · 🇨🇴 11h · 🇦🇷 13h · 🇪🇸 18h — Demo técnica + repo incluido + desbloqueo en directo del Curso Harness Engineering & SDD.")
