# StrafeKit(In Progress)

**A modular pentesting framework that automates the recon-to-exploitation loop across full engagements.**
StrafeKit unifies the repetitive, fragmented stages of a network penetration test into a cohesive workflow. Instead of juggling loose text files and disconnected terminal tabs, StrafeKit centralizes target context across the entire assessment lifecycle.

* **Browser-Based Interface:** Manages engagements through an intuitive web UI—providing a centralized dashboard for orchestration, live status tracking, and target visualization.
* **Dynamic Command Generation:** Combines user-defined TOML templates with live target data (IPs, open ports, service names) to build pre-populated, ready-to-run enumeration commands.
* **Contextual Progress Checklists:** Tracks completed enumeration steps per host and logs the security context (e.g., Unauth vs. Authenticated) under which each check was executed.


## Architecture
**Ports & Adapters Architecture:** Built on a clean hexagonal architecture, decoupling core framework logic from underlying pentesting tools. Adapters make it seamless to swap out, upgrade, or add new tools without breaking core engine workflows.
 

## Module Overview

Modules operate independently and hand off findings asynchronously through a central **SQL Datastore**. 
Tools do not call each other directly; instead, module outputs update state tables, which sequentially drive subsequent assessment phases.
![StrafeKit Architecture](./assets/architecture.jpeg)

| Module | Purpose |
| :--- | :--- |
| **NetworkScanner** | Sweeps targets to perform host discovery, port mapping, and network surface identification. |
| **WebRecon** | Handles multi-phase web reconnaissance, including spidering, parameter hunting, secret extraction, directory brute-forcing, and access control bypasses. |
| **ServiceScanner** | Identifies service misconfigurations, maps protocols, and tags known vulnerable software versions across exposed ports. |
| **BruteForce** | Executes credential attacks against web authentication forms, APIs, and network protocol services using context-driven wordlists. |
| **Cracker** | Runs offline hash cracking against recovered hashes (standalone or linked to extracted accounts) and feeds cracked passwords back into the datastore. |
| **LateralAccess** | Tests credential pairs across discovered services and hosts to validate access rights and notify on success. |
| **EngagementNotes** | Generates target-bound, copy-paste-ready command playbooks populated dynamically with live engagement data. |

