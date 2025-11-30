# System Diagrams

## Data Flow Diagram (Level 0)
```mermaid
graph LR
    User((User)) -->|Enroll / Login| Frontend[Next.js Frontend]
    Frontend -->|API Calls| API[Django REST API]
    API -->|CRUD| DB[(PostgreSQL)]
    Admin((Admin)) --> Frontend
    Registrar((Registrar)) --> Frontend
    Cashier((Cashier)) --> Frontend
    Faculty((Faculty)) --> Frontend
```

## Data Flow Diagram (Level 1) - Enrollment
```mermaid
graph LR
    Student((Student)) -->|Select Subjects| FE[Enrollment UI]
    FE -->|Request Subjects| SubjectAPI[/class_subjects endpoint/]
    SubjectAPI --> DB[(PostgreSQL)]
    FE -->|Check Schedule| ScheduleAPI[/schedule endpoint/]
    ScheduleAPI --> DB
    FE -->|Submit Enrollment| EnrollmentAPI[/student_subjects enroll/]
    EnrollmentAPI --> DB
    FE -->|Tuition Assessment| TuitionAPI[/tuition-assessment/]
    TuitionAPI --> DB
    FE -->|Payment| PaymentAPI[/payment-post/]
    PaymentAPI --> DB
    Registrar((Registrar)) -->|Approve| EnrollmentAPI
    Cashier((Cashier)) -->|Confirm Payment| PaymentAPI
```

## Use Case Diagram (Textual)
```mermaid
graph TD
    A[Admin] --> UC1[Manage System Settings]
    R[Registrar] --> UC2[Approve Enrollment]
    C[Cashier] --> UC3[Confirm Payments]
    F[Faculty] --> UC4[View Class Offerings]
    S[Student] --> UC5[Register Account]
    S --> UC6[Select Subjects]
    S --> UC7[View Schedule]
    S --> UC8[Assess Fees]
    S --> UC9[Submit Payment]
```

## Activity Diagram - Enrollment Process
```mermaid
flowchart TD
    A[Start] --> R[Student Registration]
    R --> S1[Login]
    S1 --> SS[Select Subjects]
    SS --> SC{Schedule Conflict?}
    SC -->|Yes| Fix[Adjust Selection]
    Fix --> SS
    SC -->|No| PR{Prerequisites Met?}
    PR -->|No| Fix2[Resolve / Remove Subject]
    Fix2 --> SS
    PR -->|Yes| TA[Tuition Assessment]
    TA --> EN[Submit Enrollment]
    EN --> REG{Registrar Approval}
    REG -->|Rejected| Revise[Revise Enrollment]
    Revise --> SS
    REG -->|Approved| PAY[Payment Posting]
    PAY --> CF{Full Payment?}
    CF -->|No| Partial[Record Partial Payment]
    Partial --> PAY
    CF -->|Yes| Done[Enrollment Complete]
    Done --> End[End]
```

## Notes
- ERD tables are accessed via dedicated viewsets prefixed with `erd/`.
- Tuition and payment endpoints are stubs; integrate real fee logic & finance tables when defined.
- Replace placeholder model fields in `erd_models.py` with exact schema before production.
