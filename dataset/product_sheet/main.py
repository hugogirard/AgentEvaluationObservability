"""
Generate PDF product fact sheets for bank investment products.
Products: mutual funds, GICs, ETFs offered by the bank.
Each PDF includes fund objectives, performance, MER, minimums, and risk ratings.
"""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCTS = [
    {
        "filename": "product_sheet_balanced_growth_fund.pdf",
        "title": "Balanced Growth Fund",
        "type": "Mutual Fund",
        "fund_code": "BGF-4501",
        "inception_date": "March 15, 2012",
        "objective": (
            "The Balanced Growth Fund seeks long-term capital appreciation with moderate income "
            "by investing in a diversified mix of Canadian and international equities (approximately 60%) "
            "and fixed-income securities (approximately 40%). The fund targets investors with a moderate "
            "risk tolerance and a minimum 5-year investment horizon."
        ),
        "asset_allocation": [
            ("Canadian Equities", "35%"),
            ("U.S. Equities", "15%"),
            ("International Equities", "10%"),
            ("Canadian Bonds", "25%"),
            ("Corporate Bonds", "10%"),
            ("Cash & Equivalents", "5%"),
        ],
        "performance": [
            ("1 Year", "8.2%"),
            ("3 Year (annualized)", "6.5%"),
            ("5 Year (annualized)", "7.1%"),
            ("Since Inception", "6.8%"),
        ],
        "mer": "1.85%",
        "min_initial": "$5,000",
        "min_additional": "$500",
        "risk_rating": "Low to Medium",
        "distribution_frequency": "Quarterly",
        "top_holdings": [
            ("Royal Bank of Canada", "4.2%"),
            ("Toronto-Dominion Bank", "3.8%"),
            ("Shopify Inc.", "3.1%"),
            ("Government of Canada Bond 3.25% 2028", "5.5%"),
            ("Province of Ontario Bond 2.90% 2030", "4.0%"),
        ],
        "management": "Jennifer Liu, CFA -- 12 years experience, lead portfolio manager since 2018.",
        "risks": (
            "Market risk, interest rate risk, currency risk, credit risk. The fund may "
            "underperform its benchmark during periods of high equity volatility. Past performance "
            "does not guarantee future results."
        ),
    },
    {
        "filename": "product_sheet_premium_gic_18month.pdf",
        "title": "Premium GIC -- 18 Month",
        "type": "Guaranteed Investment Certificate (GIC)",
        "fund_code": "GIC-1800",
        "inception_date": "N/A -- rolling issuance",
        "objective": (
            "The 18-Month Premium GIC offers a guaranteed fixed rate of return with full principal "
            "protection. Eligible for CDIC coverage up to applicable limits. Designed for conservative "
            "investors seeking capital preservation and predictable income."
        ),
        "asset_allocation": [
            ("Term Deposit -- Fixed Rate", "100%"),
        ],
        "performance": [
            ("Current Rate (posted)", "4.35%"),
            ("Rate Type", "Fixed, non-redeemable"),
            ("Interest Calculation", "Compounded semi-annually"),
        ],
        "mer": "N/A",
        "min_initial": "$1,000",
        "min_additional": "N/A",
        "risk_rating": "Low",
        "distribution_frequency": "At maturity or semi-annually (investor's choice)",
        "top_holdings": [],
        "management": "Managed by the bank's Treasury division.",
        "risks": (
            "Minimal risk -- principal is guaranteed. Early redemption is not permitted; the investor "
            "must hold the GIC to maturity. Inflation risk may apply if the rate of return does not "
            "exceed the rate of inflation over the holding period."
        ),
    },
    {
        "filename": "product_sheet_canadian_dividend_etf.pdf",
        "title": "Canadian Dividend ETF",
        "type": "Exchange-Traded Fund (ETF)",
        "fund_code": "CDIV",
        "inception_date": "June 1, 2016",
        "objective": (
            "The Canadian Dividend ETF aims to replicate the performance of the bank's proprietary "
            "Canadian Dividend Index, which tracks 40 high-dividend-yielding Canadian equities. "
            "The fund is suitable for income-focused investors seeking tax-efficient dividend income "
            "with moderate capital growth potential."
        ),
        "asset_allocation": [
            ("Financials", "38%"),
            ("Energy", "18%"),
            ("Utilities", "14%"),
            ("Telecommunications", "12%"),
            ("Real Estate (REITs)", "10%"),
            ("Materials", "8%"),
        ],
        "performance": [
            ("1 Year", "10.4%"),
            ("3 Year (annualized)", "8.9%"),
            ("5 Year (annualized)", "7.6%"),
            ("Since Inception", "8.1%"),
        ],
        "mer": "0.22%",
        "min_initial": "1 unit (market price ~$32.50)",
        "min_additional": "1 unit",
        "risk_rating": "Medium",
        "distribution_frequency": "Monthly",
        "top_holdings": [
            ("Royal Bank of Canada", "6.5%"),
            ("Toronto-Dominion Bank", "5.8%"),
            ("Enbridge Inc.", "5.2%"),
            ("BCE Inc.", "4.7%"),
            ("TC Energy Corp.", "4.3%"),
        ],
        "management": (
            "Passively managed. Index methodology reviewed annually by the bank's Index Committee."
        ),
        "risks": (
            "Equity market risk, sector concentration risk (financials), dividend cut risk. "
            "The fund's heavy weighting in financials and energy may lead to underperformance if "
            "those sectors decline. ETF units trade on the exchange and may trade at a premium or "
            "discount to NAV."
        ),
    },
    {
        "filename": "product_sheet_global_equity_fund.pdf",
        "title": "Global Equity Growth Fund",
        "type": "Mutual Fund",
        "fund_code": "GEG-7200",
        "inception_date": "January 10, 2015",
        "objective": (
            "The Global Equity Growth Fund seeks long-term capital appreciation by investing primarily "
            "in large-cap equities across developed and emerging markets. The fund employs a bottom-up "
            "stock selection approach with a focus on companies demonstrating sustainable earnings growth, "
            "strong competitive moats, and attractive valuations. Suitable for investors with a higher "
            "risk tolerance and a minimum 7-year investment horizon."
        ),
        "asset_allocation": [
            ("U.S. Equities", "45%"),
            ("European Equities", "20%"),
            ("Asia-Pacific Equities", "15%"),
            ("Emerging Markets", "12%"),
            ("Canadian Equities", "5%"),
            ("Cash & Equivalents", "3%"),
        ],
        "performance": [
            ("1 Year", "14.7%"),
            ("3 Year (annualized)", "11.3%"),
            ("5 Year (annualized)", "10.8%"),
            ("Since Inception", "9.6%"),
        ],
        "mer": "2.15%",
        "min_initial": "$5,000",
        "min_additional": "$500",
        "risk_rating": "Medium to High",
        "distribution_frequency": "Annually",
        "top_holdings": [
            ("Microsoft Corp.", "5.1%"),
            ("Apple Inc.", "4.3%"),
            ("ASML Holding NV", "3.2%"),
            ("Taiwan Semiconductor", "2.9%"),
            ("Novo Nordisk A/S", "2.7%"),
        ],
        "management": "David Chen, CFA, MBA -- 18 years experience, lead manager since fund inception.",
        "risks": (
            "Equity market risk, currency risk, emerging market risk, geopolitical risk. "
            "The fund may experience significant short-term volatility. Foreign holdings are "
            "subject to exchange rate fluctuations that may reduce returns when converted to CAD."
        ),
    },
    {
        "filename": "product_sheet_short_term_bond_fund.pdf",
        "title": "Short-Term Bond Fund",
        "type": "Mutual Fund",
        "fund_code": "STB-3300",
        "inception_date": "September 5, 2010",
        "objective": (
            "The Short-Term Bond Fund seeks to provide a stable stream of income with low volatility "
            "by investing in a diversified portfolio of investment-grade Canadian bonds with maturities "
            "of 1 to 5 years. The fund is designed for conservative investors who require capital "
            "stability and a short-term investment horizon of 1 to 3 years."
        ),
        "asset_allocation": [
            ("Government of Canada Bonds", "40%"),
            ("Provincial Bonds", "25%"),
            ("Investment-Grade Corporate Bonds", "30%"),
            ("Cash & Equivalents", "5%"),
        ],
        "performance": [
            ("1 Year", "4.1%"),
            ("3 Year (annualized)", "3.2%"),
            ("5 Year (annualized)", "2.8%"),
            ("Since Inception", "3.0%"),
        ],
        "mer": "0.95%",
        "min_initial": "$2,500",
        "min_additional": "$250",
        "risk_rating": "Low",
        "distribution_frequency": "Monthly",
        "top_holdings": [
            ("Government of Canada 3.00% 2026", "8.2%"),
            ("Province of Quebec 2.75% 2027", "6.1%"),
            ("Royal Bank of Canada 3.50% 2026", "4.5%"),
            ("Province of British Columbia 3.10% 2028", "4.0%"),
            ("Bell Canada 3.80% 2027", "3.5%"),
        ],
        "management": "Sarah Nguyen, CFA -- 15 years fixed-income experience, lead manager since 2019.",
        "risks": (
            "Interest rate risk (moderate -- short duration mitigates), credit risk, inflation risk. "
            "Rising interest rates will cause bond prices to decline, though the short-term nature "
            "of the portfolio limits this impact. Not suitable for investors seeking capital appreciation."
        ),
    },
]


def create_product_sheet_pdf(product: dict) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, product["title"], new_x="LMARGIN", new_y="NEXT")

    # Sub-header
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Product Type: {product['type']}  |  Fund Code: {product['fund_code']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Inception Date: {product['inception_date']}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Investment Objective
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Investment Objective", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, product["objective"])
    pdf.ln(3)

    # Asset Allocation
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Asset Allocation", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    for label, pct in product["asset_allocation"]:
        pdf.cell(100, 6, f"  {label}", new_x="RIGHT")
        pdf.cell(0, 6, pct, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Performance
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Performance", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    for label, val in product["performance"]:
        pdf.cell(100, 6, f"  {label}", new_x="RIGHT")
        pdf.cell(0, 6, val, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Key Facts
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Key Facts", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    facts = [
        ("Management Expense Ratio (MER)", product["mer"]),
        ("Minimum Initial Investment", product["min_initial"]),
        ("Minimum Additional Investment", product["min_additional"]),
        ("Risk Rating", product["risk_rating"]),
        ("Distribution Frequency", product["distribution_frequency"]),
    ]
    for label, val in facts:
        pdf.cell(100, 6, f"  {label}", new_x="RIGHT")
        pdf.cell(0, 6, val, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Top Holdings
    if product["top_holdings"]:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Top Holdings", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        for name, weight in product["top_holdings"]:
            pdf.cell(100, 6, f"  {name}", new_x="RIGHT")
            pdf.cell(0, 6, weight, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # Management
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Portfolio Management", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, product["management"])
    pdf.ln(3)

    # Risks
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Risks", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, product["risks"])
    pdf.ln(3)

    # Disclaimer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0,
        4,
        "This document is for informational purposes only and does not constitute investment advice. "
        "Past performance is not indicative of future results. Please read the fund's prospectus before investing. "
        "Commissions, trailing commissions, management fees and expenses all may be associated with mutual fund investments.",
    )

    filepath = os.path.join(OUTPUT_DIR, product["filename"])
    pdf.output(filepath)
    print(f"Generated: {filepath}")


def main():
    for product in PRODUCTS:
        create_product_sheet_pdf(product)
    print(f"\nDone -- {len(PRODUCTS)} product sheet PDFs generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
