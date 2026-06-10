"""
Generate PDF FAQ documents covering fees, minimum investments,
redemption rules, transfer procedures, and account types.
"""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

FAQ_DOCUMENTS = [
    {
        "filename": "faq_fees_and_expenses.pdf",
        "title": "Frequently Asked Questions -- Fees & Expenses",
        "last_updated": "April 15, 2025",
        "questions": [
            {
                "q": "What is a Management Expense Ratio (MER)?",
                "a": (
                    "The Management Expense Ratio (MER) is the total annual cost of managing a mutual fund "
                    "or ETF, expressed as a percentage of the fund's average net assets. It includes the "
                    "management fee, operating expenses, and applicable taxes (HST/GST). For example, a fund "
                    "with an MER of 2.00% on a $10,000 investment costs approximately $200 per year. The MER "
                    "is deducted from the fund's returns, so it is not charged separately to the investor."
                ),
            },
            {
                "q": "Are there any fees to buy or sell mutual funds?",
                "a": (
                    "Our mutual funds are available on a no-load basis -- there are no front-end or back-end "
                    "sales charges. However, if you redeem units of a fund within 30 days of purchase, a "
                    "short-term trading fee of 2% of the redemption amount will apply. This fee is paid to "
                    "the fund (not the bank) to protect long-term investors from market-timing activity."
                ),
            },
            {
                "q": "What fees apply to ETF trades?",
                "a": (
                    "ETF purchases and sales are subject to a standard trading commission of $9.99 per trade "
                    "for regular accounts. Clients enrolled in the Premier Banking Program or with household "
                    "assets exceeding $250,000 receive commission-free ETF trading. All ETF trades are also "
                    "subject to the ETF's internal MER, which is embedded in the unit price."
                ),
            },
            {
                "q": "Are there annual account fees?",
                "a": (
                    "Registered accounts (RRSP, TFSA, RESP, RRIF) have an annual administration fee of "
                    "$50 per account. This fee is waived if the combined household balance across all "
                    "investment accounts exceeds $25,000. Non-registered investment accounts have no annual "
                    "administration fee."
                ),
            },
            {
                "q": "What is the fee for transferring my account to another institution?",
                "a": (
                    "An account transfer-out fee of $150 per account applies when transferring to another "
                    "financial institution. This fee covers the administrative and regulatory costs of the "
                    "transfer. Some receiving institutions may reimburse this fee -- check with the receiving "
                    "institution before initiating the transfer."
                ),
            },
            {
                "q": "Are there fees for switching between funds?",
                "a": (
                    "Switches between mutual funds within the same fund family (our bank's funds) are free "
                    "of charge. Switches between different fund families may be treated as a redemption and "
                    "repurchase, and the short-term trading fee may apply if the original fund was held for "
                    "less than 30 days. In registered accounts, switches do not trigger tax events."
                ),
            },
            {
                "q": "What currency conversion fees apply to U.S. dollar investments?",
                "a": (
                    "When purchasing U.S.-denominated securities from a Canadian dollar account, a foreign "
                    "exchange spread of approximately 1.5% is applied to the Bank of Canada noon rate. "
                    "Clients with a U.S. dollar investment account can avoid this fee by holding and trading "
                    "in U.S. dollars directly. The Norbert's Gambit strategy is not officially supported but "
                    "is not prohibited."
                ),
            },
        ],
    },
    {
        "filename": "faq_minimum_investments.pdf",
        "title": "Frequently Asked Questions -- Minimum Investments",
        "last_updated": "April 15, 2025",
        "questions": [
            {
                "q": "What is the minimum investment for mutual funds?",
                "a": (
                    "The minimum initial investment for most of our mutual funds is $5,000 for non-registered "
                    "accounts. For registered accounts (RRSP, TFSA, RESP), the minimum initial investment is "
                    "reduced to $1,000. Subsequent contributions require a minimum of $500 for non-registered "
                    "accounts and $100 for registered accounts. Some specialty funds may have higher minimums -- "
                    "check the specific fund's product sheet."
                ),
            },
            {
                "q": "What is the minimum investment for GICs?",
                "a": (
                    "The minimum investment for GICs is $1,000 for all terms. There is no maximum limit, "
                    "though CDIC coverage is limited to $100,000 per depositor per category. GICs can be "
                    "purchased in both registered and non-registered accounts."
                ),
            },
            {
                "q": "What is the minimum investment for ETFs?",
                "a": (
                    "ETFs are traded on the stock exchange, so the minimum purchase is one unit (share). "
                    "Unit prices vary by ETF -- our Canadian Dividend ETF (CDIV) currently trades at "
                    "approximately $32.50 per unit. There is no minimum number of units required, though "
                    "trading commissions may make very small purchases uneconomical."
                ),
            },
            {
                "q": "Can I set up automatic contributions?",
                "a": (
                    "Yes. Our Pre-Authorized Contribution (PAC) plan allows you to set up automatic "
                    "weekly, bi-weekly, or monthly contributions to mutual funds. The minimum PAC amount "
                    "is $50 per contribution. PAC plans are not available for ETFs or GICs. Contact your "
                    "relationship manager or set up a PAC plan through online banking."
                ),
            },
            {
                "q": "Are the minimums different for the Managed Portfolio Program?",
                "a": (
                    "Yes. The Managed Portfolio Program requires a minimum account balance of $100,000. "
                    "This program provides discretionary portfolio management, automatic rebalancing, and "
                    "access to institutional-class fund units with lower MERs. The management fee for the "
                    "program is 1.00% of assets under management, billed quarterly."
                ),
            },
        ],
    },
    {
        "filename": "faq_redemptions_and_transfers.pdf",
        "title": "Frequently Asked Questions -- Redemptions & Transfers",
        "last_updated": "April 15, 2025",
        "questions": [
            {
                "q": "How do I redeem (sell) my mutual fund units?",
                "a": (
                    "You can redeem mutual fund units through online banking, by calling our Investment "
                    "Service Centre at 1-800-555-0199, or by visiting your branch. Redemption requests "
                    "received before 4:00 PM ET on a business day are processed at that day's closing "
                    "net asset value (NAV). Requests received after 4:00 PM are processed at the next "
                    "business day's NAV. Proceeds are typically deposited to your bank account within "
                    "1-3 business days."
                ),
            },
            {
                "q": "Can I redeem my GIC before maturity?",
                "a": (
                    "Non-redeemable GICs cannot be redeemed before maturity under any circumstances. "
                    "Redeemable GICs can be cashed after a minimum holding period of 30 days, but early "
                    "redemption may result in a reduced interest rate. Cashable GICs typically earn a "
                    "lower rate than non-redeemable GICs of the same term. Check your GIC certificate "
                    "or product sheet for specific terms."
                ),
            },
            {
                "q": "What happens when my GIC matures?",
                "a": (
                    "You will receive a maturity notice approximately 15 days before your GIC matures. "
                    "You can choose to renew the GIC for a new term, transfer the proceeds to another "
                    "investment, or deposit the funds into your bank account. If no instructions are "
                    "received by the maturity date, the GIC will automatically renew for the same term "
                    "at the then-current posted rate."
                ),
            },
            {
                "q": "How do I transfer my investments from another institution?",
                "a": (
                    "To transfer investments from another institution (transfer-in), complete Form T2033 "
                    "(for registered accounts) or our Account Transfer Request form (for non-registered "
                    "accounts). Your relationship manager can initiate the process. Transfers typically "
                    "take 2-4 weeks to complete. We will reimburse transfer-out fees charged by the "
                    "sending institution up to $150 per account for transfers of $25,000 or more."
                ),
            },
            {
                "q": "Can I transfer between my own accounts (e.g., RRSP to TFSA)?",
                "a": (
                    "Transfers between different account types are treated as a withdrawal from the source "
                    "account and a contribution to the destination account. For example, transferring from "
                    "an RRSP to a TFSA requires a taxable RRSP withdrawal and uses TFSA contribution room. "
                    "Transfers within the same account type at the same institution (e.g., TFSA to TFSA) "
                    "are processed as direct transfers and do not affect contribution room. Consult your "
                    "advisor for tax implications before making inter-account transfers."
                ),
            },
            {
                "q": "What is the process for a RRIF conversion?",
                "a": (
                    "You must convert your RRSP to a RRIF by December 31 of the year you turn 71. "
                    "You can convert earlier if you wish to begin receiving income. The minimum annual "
                    "withdrawal amount is determined by a prescribed percentage based on your age (or your "
                    "spouse's age if elected). Your relationship manager can help you set up scheduled "
                    "withdrawals on a monthly, quarterly, semi-annual, or annual basis."
                ),
            },
            {
                "q": "Are there any restrictions on how frequently I can trade?",
                "a": (
                    "There are no restrictions on ETF trading frequency, though standard commissions apply. "
                    "For mutual funds, excessive short-term trading (buying and redeeming the same fund "
                    "multiple times within a 30-day period) may result in the application of the 2% "
                    "short-term trading fee and possible restrictions on future purchases. The bank "
                    "monitors for market-timing activity in accordance with regulatory requirements."
                ),
            },
        ],
    },
    {
        "filename": "faq_account_types.pdf",
        "title": "Frequently Asked Questions -- Account Types",
        "last_updated": "April 15, 2025",
        "questions": [
            {
                "q": "What types of investment accounts do you offer?",
                "a": (
                    "We offer the following investment account types:\n\n"
                    "  - Non-Registered Investment Account: Flexible account with no contribution limits; "
                    "investment income is taxable in the year earned.\n"
                    "  - RRSP (Registered Retirement Savings Plan): Tax-deferred retirement savings; "
                    "contributions are tax-deductible.\n"
                    "  - TFSA (Tax-Free Savings Account): Investment income and withdrawals are tax-free; "
                    "annual contribution limit set by CRA.\n"
                    "  - RESP (Registered Education Savings Plan): Tax-sheltered education savings with "
                    "government grants (CESG up to $500/year).\n"
                    "  - RRIF (Registered Retirement Income Fund): Converted from RRSP; provides scheduled "
                    "retirement income with mandatory minimum withdrawals.\n"
                    "  - LIRA (Locked-In Retirement Account): Holds pension funds transferred from an employer "
                    "pension plan; subject to provincial locking-in rules."
                ),
            },
            {
                "q": "What is the 2025 TFSA contribution limit?",
                "a": (
                    "The 2025 TFSA annual contribution limit is $7,000. If you were 18 or older in 2009 "
                    "and have been a Canadian resident since then, your cumulative contribution room is "
                    "$102,000 (as of 2025). Unused contribution room carries forward. Withdrawals made in "
                    "a previous year are added back to your contribution room on January 1 of the following year."
                ),
            },
            {
                "q": "What is the RRSP contribution limit for 2025?",
                "a": (
                    "Your 2025 RRSP contribution limit is 18% of your 2024 earned income, up to a maximum "
                    "of $32,490, minus any pension adjustment. Unused contribution room from prior years "
                    "carries forward indefinitely. You can find your exact limit on your most recent CRA "
                    "Notice of Assessment or by logging into your CRA My Account."
                ),
            },
            {
                "q": "Can I hold U.S. investments in my registered accounts?",
                "a": (
                    "Yes. U.S. and international securities can be held in all registered account types. "
                    "However, be aware of the following:\n\n"
                    "  - RRSP/RRIF: U.S. dividends are exempt from the 15% U.S. withholding tax under the "
                    "Canada-U.S. Tax Treaty.\n"
                    "  - TFSA/RESP: U.S. dividends are subject to 15% U.S. withholding tax (the treaty "
                    "exemption does not apply).\n"
                    "  - Currency conversion fees apply when purchasing U.S. securities from a CAD account.\n\n"
                    "Consider opening a U.S. dollar registered account to avoid repeated currency conversions."
                ),
            },
            {
                "q": "Can I have a joint investment account?",
                "a": (
                    "Joint non-registered investment accounts are available for two or more individuals. "
                    "Registered accounts (RRSP, TFSA, RESP, RRIF, LIRA) cannot be held jointly -- they "
                    "must be in a single individual's name. For joint accounts, both parties must complete "
                    "the KYC questionnaire and agree on the investment mandate. Tax reporting is split "
                    "based on each party's contribution to the account."
                ),
            },
        ],
    },
]


def create_faq_pdf(doc: dict) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, doc["title"])

    # Last updated
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Last Updated: {doc['last_updated']}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    for i, item in enumerate(doc["questions"], 1):
        # Question
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, f"Q{i}: {item['q']}")
        pdf.ln(1)

        # Answer
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, item["a"])
        pdf.ln(5)

    # Footer
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0,
        4,
        "This FAQ is provided for general information only and does not constitute financial, tax, or legal advice. "
        "Product availability, fees, and terms are subject to change without notice. For personalized guidance, "
        "please consult your relationship manager.",
    )

    filepath = os.path.join(OUTPUT_DIR, doc["filename"])
    pdf.output(filepath)
    print(f"Generated: {filepath}")


def main():
    for doc in FAQ_DOCUMENTS:
        create_faq_pdf(doc)
    print(f"\nDone -- {len(FAQ_DOCUMENTS)} FAQ PDFs generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
