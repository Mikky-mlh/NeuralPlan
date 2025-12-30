"""
Schedule management page - SOURABH: Add CSV upload, better UI styling, and Duration column validation.
Make THIS work. Don't change the logic. You can change colors if you want, but the table must work.
"""
import streamlit as st
import pandas as pd

# Modern SaaS Dashboard CSS - Notion/Linear/Vercel Level
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Modern SaaS Color System */
    :root {
        --primary: #6366f1;
        --primary-hover: #4f46e5;
        --secondary: #8b5cf6;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: #1e293b;
        --bg-hover: #334155;
        --border: rgba(148, 163, 184, 0.1);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Clean, modern background */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Compact, dense layout */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }
    
    /* Modern card styling */
    .saas-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
        transition: all 0.2s ease;
    }
    
    .saas-card:hover {
        box-shadow: var(--shadow-lg);
        border-color: rgba(148, 163, 184, 0.2);
    }
    
    /* Strong page title */
    h1 {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    /* Subtle section headers */
    h3 {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
        margin-top: 0;
    }
    
    /* Body text */
    p {
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Primary CTA Button - Clear, prominent */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.15s ease;
        border: none;
        cursor: pointer;
        background: var(--primary);
        color: white;
        box-shadow: var(--shadow-sm);
    }
    
    .stButton > button:hover {
        background: var(--primary-hover);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    /* Upload Section - Prominent drag-and-drop zone */
    .upload-card {
        background: var(--bg-card);
        border: 2px dashed var(--border);
        border-radius: 12px;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .upload-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .upload-card:hover {
        border-color: var(--primary);
        background: var(--bg-hover);
        box-shadow: var(--shadow-lg);
    }
    
    .upload-card:hover::before {
        left: 100%;
    }
    
    .upload-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        display: block;
    }
    
    .upload-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .upload-subtitle {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    /* Modern table - Clean, scannable */
    .stDataEditor {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    /* Improved row spacing and zebra striping */
    .stDataEditor table {
        border-collapse: separate;
        border-spacing: 0;
    }
    
    .stDataEditor table tbody tr {
        transition: background-color 0.15s ease;
    }
    
    .stDataEditor table tbody tr:nth-child(even) {
        background: rgba(255, 255, 255, 0.02);
    }
    
    .stDataEditor table tbody tr:hover {
        background: var(--bg-hover) !important;
    }
    
    .stDataEditor table td,
    .stDataEditor table th {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-cancelled {
        background: rgba(239, 68, 68, 0.15);
        color: var(--error);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Clean message styling */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: var(--success);
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: var(--error);
    }
    
    .stInfo {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: var(--primary);
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: var(--warning);
    }
    
    /* File uploader - Hidden default, use custom card */
    [data-testid="stFileUploader"] {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    [data-testid="stFileUploader"] > div {
        background: transparent !important;
        border: none !important;
    }
    
    /* Schedule card container */
    .schedule-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-sm);
    }
    
    /* Compact spacing utilities */
    .mb-0 { margin-bottom: 0 !important; }
    .mb-1 { margin-bottom: 0.5rem !important; }
    .mb-2 { margin-bottom: 1rem !important; }
    .mt-2 { margin-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)


# Modern SaaS Header - Strong visual hierarchy
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1>Schedule</h1>
    <p style="color: var(--text-secondary); font-size: 0.875rem; margin-top: 0.25rem;">
        Manage your class schedule and optimize your time
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize default schedule if not exists
if 'schedule' not in st.session_state:
    st.session_state.schedule = pd.DataFrame({
        "Day": ["Monday", "Monday", "Tuesday"],
        "Time": ["10:00 AM", "2:00 PM", "9:00 AM"],
        "Subject": ["Math", "Python", "Physics"],
        "Duration": [60, 90, 60],
        "Status": ["Active", "Active", "Active"]
    })

# Upload Section - Prominent drag-and-drop zone
st.markdown("""
<div class="upload-card">
    <div class="upload-icon">📤</div>
    <div class="upload-title">Upload Schedule</div>
    <div class="upload-subtitle">Drag and drop your CSV file or click to browse</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=['csv'],
    help="Upload a CSV file with your schedule. Must include a 'Duration' column (or 'duration').",
    label_visibility="collapsed"
)

# Show loading skeleton when processing
processing = False

# Handle CSV upload (KEEP ALL EXISTING LOGIC)
if uploaded_file is not None:
    processing = True
    # Show loading skeleton
    st.markdown("""
    <div style="margin: 1rem 0;">
        <div class="skeleton" style="height: 50px; margin-bottom: 0.5rem;"></div>
        <div class="skeleton" style="height: 30px; width: 60%;"></div>
    </div>
    """, unsafe_allow_html=True)
    try:
        # Read the uploaded CSV
        df_uploaded = pd.read_csv(uploaded_file)
        
        # Normalize column names: capitalize first letter, ensure Duration exists
        df_uploaded.columns = df_uploaded.columns.str.strip()  # Remove whitespace
        
        # Check if Duration column exists (case-insensitive)
        duration_col = None
        for col in df_uploaded.columns:
            if col.lower() == 'duration':
                duration_col = col
                break
        
        # Rename Duration column to ensure it's capitalized
        if duration_col:
            df_uploaded = df_uploaded.rename(columns={duration_col: "Duration"})
        else:
            # If Duration column doesn't exist, add it with default value
            df_uploaded["Duration"] = 60
            st.warning("⚠️ 'Duration' column not found in CSV. Added with default value of 60 minutes.")
        
        # Ensure Status column exists
        if "Status" not in df_uploaded.columns:
            df_uploaded["Status"] = "Active"
        
        # Capitalize first letter of all column names (except Duration which is already correct)
        column_mapping = {}
        for col in df_uploaded.columns:
            if col != "Duration" and col.lower() != "duration":
                column_mapping[col] = col.capitalize()
        df_uploaded = df_uploaded.rename(columns=column_mapping)
        
        # Ensure Duration is numeric
        df_uploaded["Duration"] = pd.to_numeric(df_uploaded["Duration"], errors='coerce')
        df_uploaded["Duration"] = df_uploaded["Duration"].fillna(60)  # Fill NaN with default
        
        # Update session state
        st.session_state.schedule = df_uploaded
        st.success("✅ Schedule loaded successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error reading CSV file: {str(e)}")

# Ensure Duration column exists and is capitalized in current schedule (KEEP ALL EXISTING LOGIC)
duration_col_found = False
for col in st.session_state.schedule.columns:
    if col == "Duration":
        duration_col_found = True
        break
    elif col.lower() == "duration":
        st.session_state.schedule = st.session_state.schedule.rename(columns={col: "Duration"})
        duration_col_found = True
        break

if not duration_col_found:
    st.session_state.schedule["Duration"] = 60
    st.warning("⚠️ Duration column was missing. Added with default value of 60 minutes.")

# Ensure Duration is numeric
st.session_state.schedule["Duration"] = pd.to_numeric(
    st.session_state.schedule["Duration"], 
    errors='coerce'
)
st.session_state.schedule["Duration"] = st.session_state.schedule["Duration"].fillna(60)

# Schedule Section - Card-based layout
st.markdown("""
<div class="schedule-card">
    <h3>Classes</h3>
    <p style="margin-bottom: 1rem;">Click on any cell to edit. Duration must be positive.</p>
</div>
""", unsafe_allow_html=True)

# Show editable table with validation (KEEP ALL EXISTING LOGIC)
edited = st.data_editor(
    st.session_state.schedule,
    column_config={
        "Duration": st.column_config.NumberColumn(
            "Duration",
            format="%d min",
            min_value=1,
            max_value=480
        ),
        "Status": st.column_config.SelectboxColumn(
            options=["Active", "Cancelled"]
        )
    },
    use_container_width=True,
    hide_index=True
)

# Primary CTA Button - Clear, prominent
st.markdown("<div style='margin-top: 1.5rem;'>", unsafe_allow_html=True)
if st.button("Save Changes", use_container_width=True, type="primary"):
    # Validate for negative duration values
    if "Duration" in edited.columns:
        negative_durations = edited[edited["Duration"] < 0]
        if len(negative_durations) > 0:
            st.error(f"❌ Error: Found {len(negative_durations)} row(s) with negative duration values. Duration must be positive!")
        else:
            # Ensure Duration column is still capitalized after edit
            if "Duration" not in edited.columns:
                for col in edited.columns:
                    if col.lower() == "duration":
                        edited = edited.rename(columns={col: "Duration"})
                        break
            
            st.session_state.schedule = edited
            cancelled = len(edited[edited["Status"] == "Cancelled"])
            if cancelled > 0:
                st.success(f"✅ {cancelled} classes cancelled. Go to Neural Coach!")
            else:
                st.info("All classes active.")
    else:
        st.error("❌ Error: Duration column is missing from the schedule!")
st.markdown("</div>", unsafe_allow_html=True)

# Add JavaScript to enhance table with status pills
st.markdown("""
<script>
    // Enhance status cells with pills after table renders
    function enhanceStatusPills() {
        const tables = document.querySelectorAll('.stDataEditor table');
        tables.forEach(table => {
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                cells.forEach((cell, index) => {
                    const header = table.querySelectorAll('thead th')[index];
                    if (header && header.textContent.trim() === 'Status') {
                        const status = cell.textContent.trim();
                        if (status === 'Active' || status === 'Cancelled') {
                            cell.innerHTML = `<span class="status-pill status-${status.toLowerCase()}">${status}</span>`;
                        }
                    }
                });
            });
        });
    }
    
    // Run on load and after Streamlit updates
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', enhanceStatusPills);
    } else {
        enhanceStatusPills();
    }
    
    const observer = new MutationObserver(enhanceStatusPills);
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)