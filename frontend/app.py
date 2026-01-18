import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import os
import plotly.express as px
import plotly.graph_objects as go

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.database_utils import (
    get_all_books, add_book, update_book, delete_book, 
    borrow_book, return_book, get_borrowing_history, get_overdue_books
)

st.set_page_config(
    page_title="Library Pro | Premium", 
    layout="wide", 
    page_icon="📖",
    initial_sidebar_state="expanded"
)

# Sophisticated Dark Design System
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }

    /* Global Dark Background */
    .stApp {
        background-color: #0f172a;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0c111d;
        border-right: 1px solid #1e293b;
    }
    
    /* Consolidated Navigation Styling */
    div[data-testid="stRadio"] > label {
        display: none;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding-top: 10px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background: transparent;
        border-radius: 12px;
        padding: 12px 16px !important;
        margin: 0 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border: 1px solid transparent;
        display: flex !important;
        align-items: center;
        width: 100%;
        color: #94a3b8;
    }
    
    /* Hide standard radio circle */
    div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }
    
    /* Text styling */
    div[data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        font-weight: 500;
        letter-spacing: 0.02em;
        font-size: 0.95rem;
    }
    
    /* Hover State */
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        transform: translateX(4px);
    }
    
    /* Active State */
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
        background: rgba(99, 102, 241, 0.08) !important;
        color: #818cf8 !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        font-weight: 600;
        box-shadow: 0 4px 12px -2px rgba(99, 102, 241, 0.1);
    }

    /* Targetting labels to insert icons via pseudo-elements */
    div[data-testid="stRadio"] div[role="radiogroup"] label:nth-child(1)::before { content: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'); margin-right: 12px; display: flex; align-items: center; }
    div[data-testid="stRadio"] div[role="radiogroup"] label:nth-child(2)::before { content: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M21 8V21H3V8"/><path d="M1 3H23V8H1z"/><path d="M10 12H14"/></svg>'); margin-right: 12px; display: flex; align-items: center; }
    div[data-testid="stRadio"] div[role="radiogroup"] label:nth-child(3)::before { content: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>'); margin-right: 12px; display: flex; align-items: center; }
    div[data-testid="stRadio"] div[role="radiogroup"] label:nth-child(4)::before { content: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><rect x="1" y="3" width="15" height="13"/><polyline points="16 8 20 8 23 11 23 16 16 16"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>'); margin-right: 12px; display: flex; align-items: center; }
    
    /* Change icon color on active */
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"]::before {
        filter: invert(53%) sepia(85%) saturate(1478%) hue-rotate(210deg) brightness(101%) contrast(92%);
    }

    /* Luxury Dark Metrics */
    [data-testid="stMetric"] {
        background: #111827;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        border: 1px solid #1e293b;
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        background: #1f2937;
        border-color: #6366f1;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Glassmorphism Cards */
    .premium-card {
        background: rgba(17, 24, 39, 0.6);
        backdrop-filter: blur(12px);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #1e293b;
        color: #f8fafc;
        margin-bottom: 20px;
    }
    .premium-card h3, .premium-card h2 {
        color: #ffffff !important;
        margin-top: 0;
        letter-spacing: -0.01em;
    }
    
    .status-badge {
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .status-overdue { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
    .status-active { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    
    /* Styled Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: #0c111d !important;
        color: white !important;
        border-color: #1e293b !important;
        border-radius: 12px !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Minimalistic Icon Set
def get_icon_svg(name):
    icons = {
        "dashboard": '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
        "inventory": '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8V21H3V8"/><path d="M1 3H23V8H1z"/><path d="M10 12H14"/></svg>',
        "issuance": '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>',
        "logistics": '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polyline points="16 8 20 8 23 11 23 16 16 16"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
        "kpi_total": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
        "kpi_stock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        "kpi_circ": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
        "kpi_crit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "alert": '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
    }
    return icons.get(name, "")

# Session State for Navigation & Notifications
if 'menu' not in st.session_state:
    st.session_state.menu = "Dashboard"
if 'toast' not in st.session_state:
    st.session_state.toast = None

# Notification Dispatcher
if st.session_state.toast:
    st.toast(st.session_state.toast['text'], icon=st.session_state.toast['icon'])
    st.session_state.toast = None

def update_menu():
    st.session_state.menu = st.session_state.nav_radio

with st.sidebar:
    st.markdown(f"""
        <div style="padding: 20px 0; text-align: left; margin-bottom: 24px;">
            <div style="color: #6366f1; font-size: 0.7rem; letter-spacing: 0.25em; font-weight: 700; margin-bottom: 8px; opacity: 0.8;">CORE ARCHIVE</div>
            <h1 style="color: #ffffff; font-size: 1.5rem; font-weight: 800; margin: 0; letter-spacing: -0.02em;">LIBRARY PRO</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Using standard elements but making them look custom
    menu_options = ["Dashboard", "Inventory", "Issuance", "Logistics"]
    
    # We use st.radio and style it as blocks via the global CSS in st.markdown
    selected = st.radio(
        "Navigation",
        menu_options,
        index=menu_options.index(st.session_state.menu),
        label_visibility="collapsed",
        key="nav_radio",
        on_change=update_menu
    )

menu = st.session_state.menu

if menu == "Dashboard":
    st.title("📊 Enterprise Overview")
    
    books = get_all_books() or []
    active_borrows = get_borrowing_history(only_active=True) or []
    overdue = get_overdue_books() or []
    
    # Custom Luxury Metrics
    total_assets = sum(b['total_quantity'] for b in books)
    available_assets = sum(b['available_quantity'] for b in books)
    circulating = len(active_borrows)
    overdue_count = len(overdue)

    # Updated KPI Card to use SVGs
    def kpi_card(label, value, icon_name, color="#6366f1"):
        icon_svg = get_icon_svg(icon_name)
        return f"""
            <div style="
                background: #111827;
                border: 1px solid #1f2937;
                border-radius: 16px;
                padding: 24px;
                display: flex;
                flex-direction: column;
                gap: 15px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            ">
                <div style="color: {color}; width: 24px; height: 24px;">{icon_svg}</div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
                    <div style="color: #ffffff; font-size: 1.75rem; font-weight: 800; margin-top: 4px;">{value}</div>
                </div>
            </div>
        """

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(kpi_card("Total Assets", total_assets, "kpi_total", "#6366f1"), unsafe_allow_html=True)
    m2.markdown(kpi_card("Availability", available_assets, "kpi_stock", "#10b981"), unsafe_allow_html=True)
    m3.markdown(kpi_card("Circulating", circulating, "kpi_circ", "#f59e0b"), unsafe_allow_html=True)
    m4.markdown(kpi_card("Overdue", overdue_count, "kpi_crit", "#ef4444"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphical Representations
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.subheader("📈 Portfolio Distribution")
        if books:
            df_books = pd.DataFrame(books)
            fig = px.bar(
                df_books, 
                x="title", 
                y=["available_quantity", "total_quantity"],
                barmode="group",
                color_discrete_sequence=["#6366f1", "rgba(99, 102, 241, 0.15)"],
                labels={"value": "Units", "title": "Asset Title", "variable": "Status"},
                template="plotly_dark"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=20, b=20),
                height=400,
                bargap=0.3,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Insufficient data for visual analytics.")

    with c2:
        st.subheader("🔔 Intelligence Feed")
        if overdue:
            for item in overdue[:4]:
                st.markdown(f"""
                    <div style="padding:15px; border-radius:12px; background:rgba(30,39,59,0.5); border: 1px solid #1e293b; margin-bottom:12px; display:flex; align-items:center; gap:15px;">
                        <div style="color:#ef4444; width:20px; height:20px;">{get_icon_svg("alert")}</div>
                        <div>
                            <div style="font-weight:700; color:white; font-size:0.85rem;">{item['title']}</div>
                            <div style="color:#94a3b8; font-size:0.7rem;">Held by {item['borrower_name']} • Due {item['due_date']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="premium-card" style="text-align:center; padding:50px 20px; border-style: dashed; border-color: #1e293b; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <div style="color: #6366f1; width: 40px; height: 40px; margin-bottom: 15px;">{get_icon_svg("kpi_stock")}</div>
                    <div style="font-weight:700; color: #ffffff; letter-spacing: 0.1em; font-size: 0.75rem; text-transform: uppercase;">System Stable</div>
                    <div style="color: #94a3b8; font-size: 0.7rem; margin-top: 5px;">No critical assets detected.</div>
                </div>
            """, unsafe_allow_html=True)
            
        # Refined Donut Chart
        if books:
            avail = sum(b['available_quantity'] for b in books)
            total = sum(b['total_quantity'] for b in books)
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Available', 'Issued'], 
                values=[avail, total-avail],
                hole=.75,
                marker_colors=["#6366f1", "rgba(255,255,255,0.05)"],
                textinfo='none'
            )])
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=0, b=0),
                height=220,
                showlegend=False,
                annotations=[dict(text=f"{int(avail/total*100 if total>0 else 0)}%", x=0.5, y=0.5, font_size=20, font_color="#6366f1", showarrow=False)]
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

elif menu == "Inventory":
    st.title("📦 Asset Inventory")
    
    books = get_all_books() or []
    total_titles = len(books)
    in_stock = sum(1 for b in books if b['available_quantity'] > 0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="premium-card">
                <small style="color:#94a3b8; font-weight:600;">PORTFOLIO HEALTH</small>
                <h2 style="margin:10px 0; color:#ffffff !important;">{in_stock} / {total_titles}</h2>
                <p style="color:#94a3b8; font-size:0.9rem;">Titles currently available for checkout.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="premium-card">
                <small style="color:#94a3b8; font-weight:600;">ACTION REQUIRED</small>
                <h2 style="margin:10px 0; color:#ffffff !important;">{total_titles - in_stock}</h2>
                <p style="color:#94a3b8; font-size:0.9rem;">Titles currently out of stock.</p>
            </div>
        """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["✨ Asset Registry", "➕ Register New Title"])
    
    with tab1:
        if books:
            df = pd.DataFrame(books)
            df['Status'] = df['available_quantity'].apply(lambda x: "🟢 Available" if x > 0 else "🔴 Out of Stock")
            df = df[['id', 'title', 'author', 'total_quantity', 'available_quantity', 'Status']]
            
            st.dataframe(
                df, 
                use_container_width=True,
                column_config={
                    "id": st.column_config.NumberColumn("ID", width="small"),
                    "total_quantity": st.column_config.NumberColumn("Total"),
                    "available_quantity": st.column_config.NumberColumn("Available")
                },
                hide_index=True
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🛠️ Advanced Asset Control"):
                book_to_edit = st.selectbox("Select Asset to Modify", [f"{b['id']}: {b['title']}" for b in books])
                if book_to_edit:
                    bid = int(book_to_edit.split(":")[0])
                    orig = next(b for b in books if b['id'] == bid)
                    
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        new_title = st.text_input("Refined Title", value=orig['title'])
                        new_author = st.text_input("Verified Author", value=orig['author'])
                    with ec2:
                        new_qty = st.number_input("Adjust Total Stock", min_value=orig['total_quantity'] - orig['available_quantity'], value=orig['total_quantity'])
                        st.markdown("<br>", unsafe_allow_html=True)
                        b1, b2 = st.columns(2)
                        if b1.button("Update Registry", use_container_width=True):
                            update_book(bid, new_title, new_author, orig['isbn'], int(new_qty))
                            st.session_state.toast = {"text": f"✅ Asset '{new_title}' updated successfully!", "icon": "📦"}
                            st.rerun()
                        if b2.button("Decommission", use_container_width=True):
                            delete_book(bid)
                            st.session_state.toast = {"text": "🗑️ Asset decommissioned.", "icon": "⚠️"}
                            st.rerun()
        else:
            st.info("Registry is empty.")

    with tab2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        with st.form("add_book_form", clear_on_submit=True):
            st.subheader("New Asset Registration")
            ft1, ft2 = st.columns(2)
            t = ft1.text_input("Official Title")
            a = ft1.text_input("Lead Author")
            i = ft2.text_input("ISBN Identifier (Optional)")
            q = ft2.number_input("Initial Stock Quantity", min_value=1, value=1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Complete Registration", use_container_width=True):
                if t and a:
                    add_book(t, a, i, int(q))
                    st.session_state.toast = {"text": f"✨ New asset '{t}' registered!", "icon": "📖"}
                    # The form submit clears the form, st.success is fine here if we don't rerun
                    # But since we want consistent toasts across sections, we can use the toast state
                    st.success(f"Successfully registered '{t}'")
                else:
                    st.error("Missing required registration fields.")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Issuance":
    st.title("🤝 Asset Circulation")
    
    books = get_all_books() or []
    avail_books = [b for b in books if b['available_quantity'] > 0]
    
    if not avail_books:
        st.warning("All inventory is currently circulating.")
    else:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        with st.form("borrow_form", clear_on_submit=True):
            st.subheader("Asset Issuance Protocol")
            book_sel = st.selectbox("Select Asset", [f"{b['id']}: {b['title']} ({b['available_quantity']} units)" for b in avail_books])
            
            c1, c2 = st.columns(2)
            name = c1.text_input("Recipient Full Name")
            contact = c1.text_input("Recipient Contact")
            
            days = c2.slider("Period (Days)", 1, 30, 7)
            due = date.today() + timedelta(days=days)
            c2.info(f"Target Return: {due}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Authorize Issuance", use_container_width=True):
                if name and contact:
                    bid = int(book_sel.split(":")[0])
                    borrow_book(bid, name, contact, due)
                    st.session_state.toast = {"text": f"🤝 Asset issued to {name}", "icon": "📤"}
                    st.rerun()
                else:
                    st.error("Required fields missing.")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Logistics":
    st.title("📅 Returns & Dispatch")
    
    borrows = get_borrowing_history(only_active=True)
    if borrows:
        for b in borrows:
            is_overdue = b['due_date'] < date.today()
            status_class = "status-overdue" if is_overdue else "status-active"
            status_label = "CRITICAL" if is_overdue else "TRACKING"
            
            st.markdown(f"""
                <div class="premium-card">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <div>
                            <span class="status-badge {status_class}">{status_label}</span>
                            <h3 style="margin:10px 0 5px 0;">{b['title']}</h3>
                            <p style="color:#94a3b8; margin:0; font-size:0.9rem;">
                                👤 {b['borrower_name']} &nbsp;•&nbsp; 📱 {b['borrower_contact']}
                            </p>
                        </div>
                        <div style="text-align:right;">
                            <small style="color:#94a3b8;">SCHEDULED RETURN</small><br>
                            <span style="font-weight:700; color:{'#fca5a5' if is_overdue else '#6366f1'}">{b['due_date']}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns([1, 4])
            if btn_col1.button("Acknowledge Return", key=f"ret_{b['borrowing_id']}", use_container_width=True):
                return_book(b['book_id'], b['borrowing_id'])
                st.session_state.toast = {"text": f"📥 Return acknowledged for {b['title']}", "icon": "✅"}
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("No active circulation records.")
