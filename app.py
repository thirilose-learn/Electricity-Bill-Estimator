# pyrefly: ignore [missing-import]
import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple

# ----------------------------------------------------
# Calculation & Core Logic Functions
# ----------------------------------------------------

def calculate_flat_bill(units: float, flat_rate: float, base_charge: float) -> Tuple[float, float]:
    """
    Computes the electricity bill using a single flat rate.
    
    Args:
        units (float): The energy consumed in kWh.
        flat_rate (float): The cost per unit of energy.
        base_charge (float): The fixed customer charge.
        
    Returns:
        tuple[float, float]: Total bill and consumption charge.
    """
    if units is None or flat_rate is None or base_charge is None:
        raise ValueError("All input fields must be filled.")
    
    if units < 0 or flat_rate < 0 or base_charge < 0:
        raise ValueError("Inputs cannot be negative. Please enter valid positive values.")

    consumption_charge = units * flat_rate
    total_bill = consumption_charge + base_charge
    return total_bill, consumption_charge

def calculate_slab_bill(units: float, slab1_limit: float, slab1_rate: float, slab2_limit: float, slab2_rate: float, slab3_rate: float, base_charge: float) -> Tuple[float, float, str]:
    """
    Computes the electricity bill using a progressive slab-based model.
    
    Args:
        units (float): The energy consumed in kWh.
        slab1_limit (float): Upper limit for the first slab.
        slab1_rate (float): Rate for the first slab.
        slab2_limit (float): Upper limit for the second slab.
        slab2_rate (float): Rate for the second slab.
        slab3_rate (float): Rate for anything above slab 2 limit.
        base_charge (float): Fixed customer charge.
        
    Returns:
        tuple[float, float, str]: Total bill, consumption charge, and a breakdown string.
    """
    if None in (units, slab1_limit, slab1_rate, slab2_limit, slab2_rate, slab3_rate, base_charge):
        raise ValueError("All input fields must be filled.")
        
    if units < 0 or base_charge < 0 or slab1_limit < 0 or slab2_limit < 0:
        raise ValueError("Values cannot be negative. Please enter valid positive values.")
        
    if slab1_limit >= slab2_limit:
        raise ValueError("Slab 1 limit must be strictly less than Slab 2 limit.")
        
    if slab1_rate < 0 or slab2_rate < 0 or slab3_rate < 0:
        raise ValueError("Rates cannot be negative.")

    breakdown = []
    consumption_charge = 0.0
    remaining_units = units

    # Slab 1
    slab1_units = min(remaining_units, slab1_limit)
    if slab1_units > 0:
        charge = slab1_units * slab1_rate
        consumption_charge += charge
        breakdown.append(f"Slab 1 (0-{slab1_limit} kWh): {slab1_units:.1f} kWh @ ₹{slab1_rate:.3f}/kWh = ₹{charge:.2f}")
        remaining_units -= slab1_units

    # Slab 2
    if remaining_units > 0:
        slab2_capacity = slab2_limit - slab1_limit
        slab2_units = min(remaining_units, slab2_capacity)
        if slab2_units > 0:
            charge = slab2_units * slab2_rate
            consumption_charge += charge
            breakdown.append(f"Slab 2 ({slab1_limit}-{slab2_limit} kWh): {slab2_units:.1f} kWh @ ₹{slab2_rate:.3f}/kWh = ₹{charge:.2f}")
            remaining_units -= slab2_units

    # Slab 3
    if remaining_units > 0:
        charge = remaining_units * slab3_rate
        consumption_charge += charge
        breakdown.append(f"Slab 3 (>{slab2_limit} kWh): {remaining_units:.1f} kWh @ ₹{slab3_rate:.3f}/kWh = ₹{charge:.2f}")

    total_bill = consumption_charge + base_charge
    breakdown_text = "\n".join(breakdown) if breakdown else "No consumption charge applied (0 kWh)."
    return total_bill, consumption_charge, breakdown_text

# ----------------------------------------------------
# Gradio Tab Integrations & Formatting
# ----------------------------------------------------

def basic_calculator(units: float, flat_rate: float, base_charge: float) -> str:
    try:
        total, consumption = calculate_flat_bill(units, flat_rate, base_charge)
        return (
            f"### Total Bill: **₹{total:.2f}**\n\n"
            f"**Breakdown:**\n"
            f"- Base Customer Charge: ₹{base_charge:.2f}\n"
            f"- Energy Consumption Charge ({units:.1f} kWh @ ₹{flat_rate:.3f}/kWh): ₹{consumption:.2f}"
        )
    except Exception as e:
        return f"⚠️ **Error:** {str(e)}"

def slab_calculator(units: float, slab1_limit: float, slab1_rate: float, slab2_limit: float, slab2_rate: float, slab3_rate: float, base_charge: float) -> str:
    try:
        total, consumption, breakdown = calculate_slab_bill(
            units, slab1_limit, slab1_rate, slab2_limit, slab2_rate, slab3_rate, base_charge
        )
        return (
            f"### Total Bill: **₹{total:.2f}**\n\n"
            f"**Breakdown:**\n"
            f"- Base Customer Charge: ₹{base_charge:.2f}\n"
            f"{breakdown}\n"
            f"- Total Energy Consumption Charge: ₹{consumption:.2f}"
        )
    except Exception as e:
        return f"⚠️ **Error:** {str(e)}"

def generate_comparison_charts(mode: str, jan: float, feb: float, mar: float, apr: float, may: float, jun: float, jul: float, aug: float, sep: float, oct: float, nov: float, dec: float, flat_rate: float, slab1_limit: float, slab1_rate: float, slab2_limit: float, slab2_rate: float, slab3_rate: float, base_charge: float) -> Tuple[go.Figure, str]:
    try:
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        usages = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
        
        if mode == "6-Month Dashboard":
            months = months[:6]
            usages = usages[:6]

        # Validate inputs
        if any(u is None or u < 0 for u in usages):
            raise ValueError("All monthly usages must be filled and non-negative.")
        if flat_rate is None or base_charge is None:
            raise ValueError("Flat rate and base charge are required for comparison.")
        
        flat_bills = []
        slab_bills = []

        for u in usages:
            flat_tot, _ = calculate_flat_bill(u, flat_rate, base_charge)
            slab_tot, _, _ = calculate_slab_bill(u, slab1_limit, slab1_rate, slab2_limit, slab2_rate, slab3_rate, base_charge)
            flat_bills.append(flat_tot)
            slab_bills.append(slab_tot)

        # Create interactive Plotly figure
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Monthly Energy Consumption (kWh)", "Monthly Estimated Cost Comparison (₹)"),
            horizontal_spacing=0.15
        )

        # Plot 1: Monthly Consumption
        fig.add_trace(
            go.Bar(
                x=months,
                y=usages,
                name="Consumption (kWh)",
                marker_color="#10b981", # Emerald
                text=usages,
                textposition='auto',
                hovertemplate="Month: %{x}<br>Consumption: %{y} kWh<extra></extra>"
            ),
            row=1, col=1
        )

        # Plot 2: Cost Comparison
        fig.add_trace(
            go.Scatter(
                x=months,
                y=flat_bills,
                mode="lines+markers",
                name="Flat Rate Model",
                line=dict(color="#f59e0b", width=3), # Amber
                marker=dict(size=8),
                hovertemplate="Month: %{x}<br>Flat Bill: ₹%{y:.2f}<extra></extra>"
            ),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(
                x=months,
                y=slab_bills,
                mode="lines+markers",
                name="Slab Pricing Model",
                line=dict(color="#3b82f6", width=3, dash='dash'), # Blue
                marker=dict(size=8),
                hovertemplate="Month: %{x}<br>Slab Bill: ₹%{y:.2f}<extra></extra>"
            ),
            row=1, col=2
        )

        # Style layout for premium glassmorphism/dark theme look
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(15, 23, 42, 0.8)', # Tailwind Slate-900 with opacity
            plot_bgcolor='rgba(15, 23, 42, 0.8)',
            font=dict(family="Outfit, Inter, sans-serif", color="#f8fafc"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=40, r=40, t=50, b=40),
            height=450
        )

        fig.update_xaxes(showgrid=False, title_font=dict(size=12))
        fig.update_yaxes(showgrid=True, gridcolor="#334155", title_font=dict(size=12))

        # Calculate metrics summaries
        total_usage = sum(usages)
        avg_usage = total_usage / len(usages)
        total_flat_cost = sum(flat_bills)
        total_slab_cost = sum(slab_bills)
        savings = total_flat_cost - total_slab_cost
        cheaper_model = "Slab Pricing" if savings > 0 else "Flat Rate"
        abs_savings = abs(savings)

        title = "12-Month Annual Summary Analysis" if mode == "12-Month Dashboard" else "6-Month Summary Analysis"
        summary_html = f"""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 20px;">
            <h4 style="margin-top: 0; margin-bottom: 15px; color: #38bdf8;">📊 {title}</h4>
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 15px;">
                <div style="flex: 1; min-width: 150px;">
                    <div style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">⚡ Total Consumption</div>
                    <div style="font-size: 20px; font-weight: bold; color: #10b981;">{total_usage:.1f} kWh</div>
                </div>
                <div style="flex: 1; min-width: 150px; border-left: 1px solid #334155; padding-left: 15px;">
                    <div style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">📈 Average Monthly Consumption</div>
                    <div style="font-size: 18px; font-weight: bold; color: #38bdf8;">{avg_usage:.1f} kWh/month</div>
                </div>
                <div style="flex: 1; min-width: 150px; border-left: 1px solid #334155; padding-left: 15px;">
                    <div style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">💰 Total Cost (Flat Rate)</div>
                    <div style="font-size: 20px; font-weight: bold; color: #f59e0b;">₹{total_flat_cost:.2f}</div>
                </div>
                <div style="flex: 1; min-width: 150px; border-left: 1px solid #334155; padding-left: 15px;">
                    <div style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">💵 Total Cost (Slab Pricing)</div>
                    <div style="font-size: 20px; font-weight: bold; color: #3b82f6;">₹{total_slab_cost:.2f}</div>
                </div>
                <div style="flex: 1; min-width: 200px; border-left: 1px solid #334155; padding-left: 15px;">
                    <div style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">⭐ Recommendation</div>
                    <div style="font-size: 16px; font-weight: bold; color: #34d399;">{cheaper_model} is more economical by ₹{abs_savings:.2f}!</div>
                </div>
            </div>
        </div>
        """

        return fig, summary_html

    except Exception as e:
        # Return an empty graph and error text
        return go.Figure(), f"⚠️ **Error generating dashboard:** {str(e)}"

# ----------------------------------------------------
# UI Definition using Gradio Blocks
# ----------------------------------------------------

# Custom CSS for rich aesthetics and clean spacing
custom_css = """
body {
    background-color: #0f172a !important;
}
.gradio-container {
    font-family: 'Outfit', 'Inter', sans-serif !important;
}
.header-box {
    text-align: center;
    padding: 30px;
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    border-radius: 12px;
    border: 1px solid #312e81;
    margin-bottom: 25px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}
.header-box h1 {
    color: #38bdf8 !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    margin-bottom: 8px !important;
}
.header-box p {
    color: #94a3b8 !important;
    font-size: 1.1rem !important;
}
"""

with gr.Blocks() as demo:
    
    # Premium Header Card
    gr.HTML(
        """
        <div class="header-box">
            <h1>⚡ Smart Electricity Bill Estimator</h1>
            <p>Calculate your expected utility bills, explore tiered slab pricing, and analyze your consumption trends through our interactive comparison dashboard.</p>
        </div>
        """
    )
    
    # Global Settings (Collapsible to keep UI clean)
    with gr.Accordion("⚙️ Global Price Config & Base Fees", open=True):
        gr.Markdown("Configure pricing variables here to apply to both calculators and the monthly comparison tab.")
        with gr.Row():
            global_base = gr.Number(value=15.00, label="Fixed Base Charge (₹)", precision=2)
            global_flat_rate = gr.Number(value=0.150, label="Flat Rate (₹/kWh)", precision=3)
        
        with gr.Row():
            gr.Markdown("### Slab Tiers Configuration")
        with gr.Row():
            slab1_lim = gr.Number(value=100, label="Slab 1 Limit (kWh)", precision=0)
            slab1_rt = gr.Number(value=0.100, label="Slab 1 Rate (₹/kWh)", precision=3)
        with gr.Row():
            slab2_lim = gr.Number(value=300, label="Slab 2 Limit (kWh)", precision=0)
            slab2_rt = gr.Number(value=0.140, label="Slab 2 Rate (₹/kWh)", precision=3)
            slab3_rt = gr.Number(value=0.200, label="Slab 3 Rate (₹/kWh)", precision=3)

    # Main Tab Control
    with gr.Tabs():
        
        # 1. Flat Rate Tab
        with gr.TabItem("🔋 Basic: Flat Rate"):
            gr.Markdown("Estimate your bill based on a simple flat energy rate model.")
            with gr.Row():
                with gr.Column(scale=1):
                    flat_units = gr.Number(label="Energy Consumed (kWh)", value=250, minimum=0)
                    calc_flat_btn = gr.Button("Calculate Flat Bill", variant="primary")
                with gr.Column(scale=1):
                    flat_output = gr.Markdown("### Results will appear here after calculation.")
            
            calc_flat_btn.click(
                fn=basic_calculator,
                inputs=[flat_units, global_flat_rate, global_base],
                outputs=flat_output
            )

        # 2. Slab Pricing Tab
        with gr.TabItem("🪜 Intermediate: Slab pricing"):
            gr.Markdown("Estimate your bill using progressive/slab tier billing structure.")
            with gr.Row():
                with gr.Column(scale=1):
                    slab_units = gr.Number(label="Energy Consumed (kWh)", value=350, minimum=0)
                    calc_slab_btn = gr.Button("Calculate Slab Bill", variant="primary")
                with gr.Column(scale=1):
                    slab_output = gr.Markdown("### Results will appear here after calculation.")
            
            calc_slab_btn.click(
                fn=slab_calculator,
                inputs=[slab_units, slab1_lim, slab1_rt, slab2_lim, slab2_rt, slab3_rt, global_base],
                outputs=slab_output
            )

        # 3. Monthly Comparison Dashboard Tab
        with gr.TabItem("📈 Extended: Monthly Dashboard"):
            gr.Markdown("Enter your monthly energy usage to visualize costs and analyze which pricing model is best for you.")
            
            dash_mode = gr.Radio(["12-Month Dashboard", "6-Month Dashboard"], value="12-Month Dashboard", label="Dashboard Type")
            
            gr.Markdown("#### Enter Monthly Energy Consumption (kWh)")
            with gr.Row():
                jan_val = gr.Slider(label="January (kWh)", minimum=0, maximum=1000, value=220, step=5)
                feb_val = gr.Slider(label="February (kWh)", minimum=0, maximum=1000, value=190, step=5)
                mar_val = gr.Slider(label="March (kWh)", minimum=0, maximum=1000, value=250, step=5)
                apr_val = gr.Slider(label="April (kWh)", minimum=0, maximum=1000, value=310, step=5)
                may_val = gr.Slider(label="May (kWh)", minimum=0, maximum=1000, value=450, step=5)
                jun_val = gr.Slider(label="June (kWh)", minimum=0, maximum=1000, value=520, step=5)
            
            with gr.Row() as h2_row:
                jul_val = gr.Slider(label="July (kWh)", minimum=0, maximum=1000, value=500, step=5)
                aug_val = gr.Slider(label="August (kWh)", minimum=0, maximum=1000, value=480, step=5)
                sep_val = gr.Slider(label="September (kWh)", minimum=0, maximum=1000, value=350, step=5)
                oct_val = gr.Slider(label="October (kWh)", minimum=0, maximum=1000, value=280, step=5)
                nov_val = gr.Slider(label="November (kWh)", minimum=0, maximum=1000, value=230, step=5)
                dec_val = gr.Slider(label="December (kWh)", minimum=0, maximum=1000, value=210, step=5)
            
            compare_btn = gr.Button("Generate Dashboard", variant="primary")
            
            summary_panel = gr.HTML("<div style='text-align: center; color: #64748b; padding-top: 20px;'>Enter data and click the button to see comparative analysis.</div>")
            comparison_plot = gr.Plot(label="Analysis Visualization")
            
            def toggle_h2(mode):
                if mode == "6-Month Dashboard":
                    return gr.update(visible=False)
                return gr.update(visible=True)
                
            dash_mode.change(fn=toggle_h2, inputs=dash_mode, outputs=h2_row)

            compare_btn.click(
                fn=generate_comparison_charts,
                inputs=[
                    dash_mode,
                    jan_val, feb_val, mar_val, apr_val, may_val, jun_val,
                    jul_val, aug_val, sep_val, oct_val, nov_val, dec_val,
                    global_flat_rate, slab1_lim, slab1_rt, slab2_lim, slab2_rt, slab3_rt, global_base
                ],
                outputs=[comparison_plot, summary_panel]
            )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(primary_hue="emerald", secondary_hue="cyan", neutral_hue="slate"),
        css=custom_css
    )
