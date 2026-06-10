"""
Generate PDF internal investment policies and suitability guidelines.
Covers risk profile definitions (conservative/moderate/aggressive),
target asset allocations, rebalancing thresholds, and compliance rules.
"""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

DOCUMENTS = [
    {
        "filename": "suitability_guidelines.pdf",
        "title": "Client Suitability Guidelines",
        "subtitle": "Investment Policy Document -- Confidential",
        "effective_date": "January 1, 2025",
        "review_date": "January 1, 2026",
        "sections": [
            {
                "heading": "1. Purpose",
                "body": (
                    "This document establishes the bank's suitability guidelines for matching "
                    "investment products to client risk profiles. All relationship managers and "
                    "investment advisors must adhere to these guidelines when making product "
                    "recommendations. Non-compliance may result in disciplinary action and regulatory "
                    "reporting obligations under CSA National Instrument 31-103."
                ),
            },
            {
                "heading": "2. Risk Profile Definitions",
                "body": (
                    "Each client must be assigned one of the following risk profiles based on their "
                    "completed Know Your Client (KYC) questionnaire. The KYC must be updated at least "
                    "every 12 months or upon a material change in client circumstances.\n\n"
                    "Conservative:\n"
                    "  - Investment horizon: 1-3 years\n"
                    "  - Risk tolerance: Low -- client cannot tolerate a decline of more than 5% in any 12-month period\n"
                    "  - Primary objective: Capital preservation and income\n"
                    "  - Suitable products: GICs, money market funds, short-term bond funds\n\n"
                    "Moderate:\n"
                    "  - Investment horizon: 3-7 years\n"
                    "  - Risk tolerance: Medium -- client can tolerate a temporary decline of up to 15%\n"
                    "  - Primary objective: Balanced growth and income\n"
                    "  - Suitable products: Balanced funds, dividend ETFs, medium-term bond funds\n\n"
                    "Aggressive:\n"
                    "  - Investment horizon: 7+ years\n"
                    "  - Risk tolerance: High -- client can tolerate a temporary decline of up to 30%\n"
                    "  - Primary objective: Long-term capital appreciation\n"
                    "  - Suitable products: Equity funds, sector ETFs, global equity funds, emerging market funds"
                ),
            },
            {
                "heading": "3. Target Asset Allocation by Risk Profile",
                "body": None,
                "table": {
                    "headers": ["Asset Class", "Conservative", "Moderate", "Aggressive"],
                    "rows": [
                        ["Canadian Equities", "5%", "25%", "40%"],
                        ["U.S. Equities", "0%", "15%", "25%"],
                        ["International Equities", "0%", "10%", "20%"],
                        ["Canadian Bonds", "50%", "25%", "5%"],
                        ["Corporate Bonds", "20%", "15%", "5%"],
                        ["Cash & Equivalents", "25%", "10%", "5%"],
                    ],
                },
            },
            {
                "heading": "4. Rebalancing Policy",
                "body": (
                    "Portfolios must be reviewed for rebalancing at least quarterly. A rebalancing event "
                    "is triggered when any asset class deviates from its target allocation by more than "
                    "the following thresholds:\n\n"
                    "  - Conservative profile: +/- 5 percentage points\n"
                    "  - Moderate profile: +/- 10 percentage points\n"
                    "  - Aggressive profile: +/- 10 percentage points\n\n"
                    "When a threshold is breached, the relationship manager must contact the client within "
                    "5 business days to discuss rebalancing options. All rebalancing recommendations must be "
                    "documented in the client file with rationale and client acknowledgment.\n\n"
                    "Automatic rebalancing is available for clients enrolled in the Managed Portfolio Program. "
                    "Clients not enrolled require explicit written consent before any trades are executed."
                ),
            },
            {
                "heading": "5. Product Concentration Limits",
                "body": (
                    "No single security may represent more than 10% of a client's total portfolio value. "
                    "No single industry sector may represent more than 25% of the equity portion of the portfolio. "
                    "These limits apply at the time of purchase; subsequent market movements may cause temporary "
                    "breaches, which must be addressed at the next quarterly review.\n\n"
                    "Exceptions require written approval from the Branch Investment Compliance Officer."
                ),
            },
            {
                "heading": "6. Suitability Override Process",
                "body": (
                    "If a client insists on a product recommendation that does not align with their risk profile, "
                    "the advisor must:\n\n"
                    "  1. Clearly explain the risks of the unsuitable investment in writing\n"
                    "  2. Obtain the client's signed acknowledgment on Form INV-42 (Unsuitability Acknowledgment)\n"
                    "  3. Submit Form INV-42 to the Branch Compliance Officer within 2 business days\n"
                    "  4. Document the interaction in the CRM system with the override reason code\n\n"
                    "The Compliance Officer will review and may escalate to Regional Compliance if the "
                    "override involves more than $250,000 or the client's full portfolio."
                ),
            },
        ],
    },
    {
        "filename": "rebalancing_policy.pdf",
        "title": "Portfolio Rebalancing Policy & Procedures",
        "subtitle": "Operations Manual -- Internal Use Only",
        "effective_date": "March 1, 2025",
        "review_date": "March 1, 2026",
        "sections": [
            {
                "heading": "1. Overview",
                "body": (
                    "This policy outlines the procedures for monitoring and rebalancing client portfolios. "
                    "Rebalancing ensures that client portfolios remain aligned with their stated investment "
                    "objectives and risk tolerance as defined in the Suitability Guidelines."
                ),
            },
            {
                "heading": "2. Monitoring Frequency",
                "body": (
                    "All client portfolios must be reviewed against target allocations on the following schedule:\n\n"
                    "  - Managed Portfolio Program accounts: Monthly (automated)\n"
                    "  - Advisory accounts (assets > $500,000): Monthly (manual review by advisor)\n"
                    "  - Advisory accounts (assets $100,000 - $500,000): Quarterly\n"
                    "  - Advisory accounts (assets < $100,000): Semi-annually\n\n"
                    "The Portfolio Analytics team generates drift reports on the first business day of each month "
                    "and distributes them to advisors via the internal dashboard."
                ),
            },
            {
                "heading": "3. Drift Thresholds and Actions",
                "body": None,
                "table": {
                    "headers": ["Drift Level", "Threshold", "Required Action", "Timeline"],
                    "rows": [
                        ["Minor", "5-9%", "Note in client file, monitor", "Next scheduled review"],
                        ["Moderate", "10-14%", "Contact client, recommend rebalancing", "5 business days"],
                        ["Significant", "15-19%", "Urgent outreach, compliance notification", "2 business days"],
                        ["Critical", ">20%", "Immediate escalation to Branch Manager", "Same day"],
                    ],
                },
            },
            {
                "heading": "4. Tax-Efficient Rebalancing",
                "body": (
                    "When rebalancing non-registered accounts, advisors must consider tax implications:\n\n"
                    "  - Prefer directing new contributions to underweight asset classes rather than selling overweight positions\n"
                    "  - Use dividend and interest income to rebalance where possible\n"
                    "  - If selling is necessary, prioritize positions with capital losses to offset gains\n"
                    "  - Document the tax rationale in the rebalancing recommendation\n\n"
                    "For RRSP, TFSA, and RESP accounts, tax considerations do not apply to trades within the account."
                ),
            },
            {
                "heading": "5. Documentation Requirements",
                "body": (
                    "All rebalancing events must be documented with:\n\n"
                    "  - Date of review and drift report reference number\n"
                    "  - Current vs. target allocation (percentage and dollar amounts)\n"
                    "  - Recommended trades with rationale\n"
                    "  - Client communication log (date, method, outcome)\n"
                    "  - Client consent confirmation (written, verbal with follow-up letter, or digital)\n"
                    "  - Trade confirmation records\n\n"
                    "Records must be retained for a minimum of 7 years per regulatory requirements."
                ),
            },
        ],
    },
    {
        "filename": "risk_scoring_methodology.pdf",
        "title": "Risk Scoring Methodology",
        "subtitle": "Quantitative Risk Assessment Framework -- Confidential",
        "effective_date": "January 1, 2025",
        "review_date": "July 1, 2025",
        "sections": [
            {
                "heading": "1. Purpose",
                "body": (
                    "This document defines the quantitative methodology used to compute portfolio risk scores. "
                    "The risk score is a numerical value from 1 (lowest risk) to 100 (highest risk) that "
                    "summarizes a portfolio's overall risk exposure relative to the bank's risk framework."
                ),
            },
            {
                "heading": "2. Risk Score Calculation",
                "body": (
                    "The risk score is computed as a weighted sum of asset class risk factors:\n\n"
                    "  Risk Score = SUM(weight_i * risk_factor_i) for each asset class i\n\n"
                    "Asset class risk factors (on a 1-100 scale):\n"
                    "  - Cash & Equivalents: 5\n"
                    "  - Government Bonds (short-term): 10\n"
                    "  - Government Bonds (long-term): 20\n"
                    "  - Investment-Grade Corporate Bonds: 25\n"
                    "  - High-Yield Bonds: 45\n"
                    "  - Canadian Equities (large-cap): 50\n"
                    "  - U.S. Equities (large-cap): 55\n"
                    "  - International Equities (developed): 60\n"
                    "  - Emerging Market Equities: 75\n"
                    "  - Sector/Thematic ETFs: 70\n"
                    "  - Alternative Investments: 80\n"
                    "  - Cryptocurrency: 95\n\n"
                    "Example: A portfolio with 60% Canadian Equities and 40% Government Bonds (short-term) "
                    "would have a risk score of: (0.60 * 50) + (0.40 * 10) = 34."
                ),
            },
            {
                "heading": "3. Risk Score Ranges and Profile Mapping",
                "body": None,
                "table": {
                    "headers": ["Risk Score Range", "Risk Profile", "Maximum Equity Exposure"],
                    "rows": [
                        ["1 - 20", "Conservative", "20%"],
                        ["21 - 45", "Moderate", "60%"],
                        ["46 - 70", "Aggressive", "90%"],
                        ["71 - 100", "Speculative (requires special approval)", "100%"],
                    ],
                },
            },
            {
                "heading": "4. Compliance Thresholds",
                "body": (
                    "A portfolio is considered out of compliance when its computed risk score exceeds "
                    "the maximum allowed score for the client's assigned risk profile:\n\n"
                    "  - Conservative clients: risk score must be <= 20\n"
                    "  - Moderate clients: risk score must be <= 45\n"
                    "  - Aggressive clients: risk score must be <= 70\n\n"
                    "If a portfolio exceeds the maximum risk score, the system flags it in the daily "
                    "compliance report and the advisor is required to take corrective action within the "
                    "timelines specified in the Rebalancing Policy."
                ),
            },
            {
                "heading": "5. Limitations",
                "body": (
                    "This risk scoring model is a simplified linear model and does not account for "
                    "correlations between asset classes, tail risk, or liquidity risk. It is intended "
                    "as a screening tool to support suitability assessments, not as a replacement for "
                    "comprehensive portfolio risk analysis. The risk factors are reviewed and updated "
                    "semi-annually by the Risk Management Committee."
                ),
            },
        ],
    },
]


def create_policy_pdf(doc: dict) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, doc["title"])

    # Subtitle
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, doc["subtitle"], new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Metadata
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Effective Date: {doc['effective_date']}  |  Next Review: {doc['review_date']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    for section in doc["sections"]:
        # Section heading
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, section["heading"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Body text
        if section.get("body"):
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, section["body"])
            pdf.ln(3)

        # Table (if present)
        if section.get("table"):
            table = section["table"]
            col_count = len(table["headers"])
            col_width = (pdf.w - pdf.l_margin - pdf.r_margin) / col_count

            # Header row
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(220, 220, 220)
            for header in table["headers"]:
                pdf.cell(col_width, 7, header, border=1, fill=True)
            pdf.ln()

            # Data rows
            pdf.set_font("Helvetica", "", 9)
            for row in table["rows"]:
                for cell_val in row:
                    pdf.cell(col_width, 7, cell_val, border=1)
                pdf.ln()
            pdf.ln(4)

    # Footer disclaimer
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0,
        4,
        "CONFIDENTIAL -- This document is the property of the bank and is intended for internal use only. "
        "Unauthorized distribution or reproduction is strictly prohibited. All policies are subject to "
        "regulatory requirements and may be updated without prior notice.",
    )

    filepath = os.path.join(OUTPUT_DIR, doc["filename"])
    pdf.output(filepath)
    print(f"Generated: {filepath}")


def main():
    for doc in DOCUMENTS:
        create_policy_pdf(doc)
    print(f"\nDone -- {len(DOCUMENTS)} internal policy PDFs generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
