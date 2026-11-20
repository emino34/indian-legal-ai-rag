# Indian Law RAG Source Guide

**Purpose:** a source and ingestion guide for building an Indian-law retrieval corpus.
**Prepared:** 17 November 2026
**Status:** starting point; this file is not a complete or authoritative statement of Indian law.

## Important scope note

There is no single static document that contains all Indian law. The corpus is spread across the Constitution, central and state legislation, rules and regulations, notifications, orders, local instruments, and judicial decisions. It changes over time; provisions may be amended, commenced on different dates, repealed, or interpreted differently by courts. India Code itself provides searchable Acts and subordinate legislation, while the Gazette of India publishes official notifications. State laws and state gazettes must also be covered for a genuinely broad collection.

Use this guide as a map for collecting primary sources. Do not treat this Markdown file as a substitute for the source instruments, legal advice, or verification of current law. A RAG answer should cite the exact source, section or paragraph, jurisdiction, and relevant date. If no authoritative source is available, say so rather than filling the gap from this guide.

## Authoritative source catalogue

Prefer the following government or court sources. Store the source URL and retrieval date with every ingested item.

| Source | What to collect | Official location |
|---|---|---|
| India Code | Central Acts, sections, rules, regulations, notifications, orders, ordinances, statutes, circulars, and related subordinate legislation published by ministries/departments | [India Code](https://www.indiacode.nic.in/indiacode/home.jsp) |
| Gazette of India | Original Acts and amendments as notified, commencement notifications, delegated legislation, and other Central Government notifications | [eGazette](https://egazette.gov.in/) |
| Legislative Department | Constitution and amendment Acts; use the latest official consolidated Constitution and retain amendment history where needed | [Constitution and documents](https://www.legislative.gov.in/documents) |
| Supreme Court of India | Supreme Court judgments and orders | [Supreme Court of India](https://www.sci.gov.in/) |
| eCourts | High Court and district court services and judgments where provided; availability and coverage vary by court | [eCourts](https://ecourts.gov.in/) |
| State and Union Territory authorities | State Acts, rules, regulations, notifications, local instruments, and state gazettes | Collect separately from the relevant official state legislature, department, or e-Gazette portal |

India Code describes its content as supplied by Government of India ministries and departments. The eGazette describes the Gazette as an authorized legal document and provides Gazette publications. A consolidated text can aid retrieval, but preserve the Gazette/source instrument because that is needed to establish enactment, amendment, commencement, and publication history.

## Coverage map

Treat these as collection areas, not a claim that every instrument has been found:

1. **Constitutional law:** Constitution of India, amendment Acts, schedules, and relevant commencement / implementation instruments.
2. **Central legislation:** current and historical Acts of Parliament, including amendment and repeal status.
3. **Delegated legislation:** central and state rules, regulations, schemes, orders, directions, notifications, and circulars. Record the parent Act and enabling provision when available.
4. **State and territorial law:** every State and Union Territory's legislation and subordinate instruments. Preserve jurisdiction because rules differ by place.
5. **Judicial decisions:** Supreme Court and relevant High Court decisions; record court, bench, case number, decision date, subsequent history, and cited provisions. Court decisions interpret law; they are not statutory text.
6. **Special and local instruments:** municipal and other local rules where in scope, plus tribunal decisions if the project intends to cover them.
7. **Historical law:** repealed, superseded, and amended texts when needed to answer questions about earlier events. Never present a historical version as current law.

## Suggested initial subject areas

Use these as retrieval tags, not as an exhaustive list of statutes:

- Constitutional and administrative law
- Criminal law and procedure; evidence
- Civil procedure, limitation, and remedies
- Contract, property, family, succession, and personal laws
- Companies, insolvency, banking, securities, and taxation
- Labour and employment
- Consumer protection and competition
- Information technology, privacy, telecommunications, and intellectual property
- Environment, land, housing, and natural resources
- Motor vehicles, transport, and infrastructure
- Education, health, food, and public welfare
- Elections, citizenship, immigration, and public order

Each area may have central, state, local, and sector-specific instruments. Avoid assuming that a subject is governed by one Act.

## Record format for each source

Keep one source instrument per record where possible. Store at least:

```yaml
record_id: stable unique identifier
title: official title as published
document_type: constitution | act | rule | regulation | notification | order | circular | judgment | other
jurisdiction: India | State/UT name | local authority
issuing_authority: ministry, legislature, court, regulator, or authority
parent_instrument: title and provision, if applicable
instrument_number: official number, if assigned
enactment_or_decision_date: YYYY-MM-DD
publication_date: YYYY-MM-DD
commencement_date: date or commencement condition, if known
effective_from: date/range, if known
effective_to: date/range or null
status: in_force | partly_in_force | amended | repealed | historical | unknown
amends_or_repeals: linked record IDs or official titles
source_url: canonical official URL
retrieved_at: YYYY-MM-DD
language: language of this text
text_version: original | amended | consolidated | translation | judgment
page_or_section: locator for this extracted passage
```

Do not infer `in_force` solely from a document's presence on a website. Verify commencement and amendment/repeal status against official instruments. Keep original text and any consolidated text as separate versions, linked together.

## RAG chunking and retrieval

- Preserve document title, jurisdiction, source URL, version date, and section/paragraph heading in every chunk's metadata.
- Split Acts and rules by section/rule, retaining the heading, provisos, explanations, illustrations, schedules, and cross-references with the relevant provision.
- Keep judgments in paragraph-sized chunks with case name, court, date, neutral/citation number where available, paragraph number, and disposition.
- Avoid combining provisions from different jurisdictions or different versions in a single chunk.
- Retrieve by jurisdiction and date as well as topic. Ask a follow-up when jurisdiction or relevant date materially changes the answer.
- Prefer primary text for quotations. Label summaries and translations as such; do not present them as the enacted text.
- Return citations that let a reviewer open the source and find the exact section or paragraph. Distinguish binding holdings from background discussion and note later history when verified.

## Update and quality workflow

1. Discover candidate instruments from the official repositories above.
2. Download or capture the original source and its metadata; save retrieval time and URL.
3. Extract text and inspect OCR for errors, especially section numbers, dates, negations, provisos, and tables.
4. Link amendments, commencement notifications, repeals, and replacement instruments to affected records.
5. Re-index each new version without deleting older versions; mark superseded records with their effective dates.
6. Periodically reconcile the corpus with official repositories and record the last checked date.
7. For an answer, retrieve the applicable version for the event date and jurisdiction, then cite primary sources. If status or commencement is uncertain, state the uncertainty.

## Limits

This guide does not contain the full text of Indian laws, all state/UT laws, every Gazette notification, or the full body of Indian case law. It does not determine whether a provision is currently in force. Official portals can have gaps, differing consolidation dates, or document/OCR problems. Verify consequential legal propositions against the original instrument and current authoritative sources.
