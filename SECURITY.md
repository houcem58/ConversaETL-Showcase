# Security Policy

## Repository Scope

This repository is a **portfolio showcase** for the ConversaETL project.

It contains:
- Architecture documentation
- Conceptual demo code with synthetic data
- Public evaluation metrics
- Research status information

It does **not** contain:
- Research implementation source code
- Compiler internals or algorithms
- Benchmark framework or evaluation engine
- Prompt engineering internals
- Schema resolution implementation
- Evaluation datasets or raw benchmark artifacts
- Private research workspace

The full research implementation is maintained in a separate private repository.

## Reporting Security Issues

If you identify a security issue in the demo code or documentation in this
repository, please contact: houcem0508@gmail.com

Do not open a public GitHub issue for security concerns.

## Demo Code

The demo code in `demo/examples/` is a standalone educational illustration.
It uses only pandas and standard Python libraries. It does not connect to
any external service, database, or API. It is safe to run in an isolated
Python environment.

## Data

All data in `demo/sample_data/` is fully synthetic. It contains no personal
information, no proprietary data, and no real customer or business records.
