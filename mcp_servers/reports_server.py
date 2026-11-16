from fastmcp import FastMCP

mcp = FastMCP("Clinic Medical Reports Server")

medical_records: dict[int, list[dict]] = {
    1: [
        {"date": "2026-10-02", "diagnosis": "Flu", "notes": "Rest"},
        {"date": "2026-10-20", "diagnosis": "Follow-up", "notes": "Recovered"},
    ],
    2: [
        {"date": "2026-09-15", "diagnosis": "Sprained ankle", "notes": "Ice and compression"},
    ],
}

opd_records: dict[int, list[dict]] = {
    1: [
        {"date": "2026-10-02", "department": "General"},
        {"date": "2026-10-20", "department": "General"},
    ],
    2: [
        {"date": "2026-09-15", "department": "Orthopedics"},
    ],
}


@mcp.tool
def get_patient_medical_records(patient_id: int) -> list[dict] | dict:
    """Return the medical records (date, diagnosis, notes) of a patient, or an error if unknown."""
    if patient_id not in medical_records:
        return {"error": f"No medical records for patient {patient_id}"}
    return medical_records[patient_id]


@mcp.tool
def get_opd_records(patient_id: int) -> list[dict] | dict:
    """Return the outpatient (OPD) visits (date, department) of a patient, or an error if unknown."""
    if patient_id not in opd_records:
        return {"error": f"No OPD records for patient {patient_id}"}
    return opd_records[patient_id]


if __name__ == "__main__":
    mcp.run(transport="http", port=8003)
