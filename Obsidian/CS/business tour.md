```mermaid.js
classDiagram
    Tour : List Travellers
    Tour: List Destiations
	Tour *-- Destination
	Destination: Str Hotel
	Destination: Guide Guide
	
	Person: Str Name
	
	Traveller <|-- Person
	Traveller: Bool hasPaid
	Guide <|-- Person
	Guide: Bool beenPaid
	
	Tour *-- Traveller
	Destination *-- Guide

```
