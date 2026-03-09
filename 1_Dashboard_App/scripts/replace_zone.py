import codecs
import re

file_path = "dashboard_app.py"
text = codecs.open(file_path, "r", "utf-8").read()

new_section_9 = """
# ==========================================
# 9. [하단] 전체 수수료 대시보드 (더블 컨테이너 레이아웃)
# ==========================================
st.markdown("<h3 style='color:#FFFFFF !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #D4AF37;'>💰 전체 수수료 대시보드 (지사수수료 기준)</h3>", unsafe_allow_html=True)

double_container_css = '''
<style>
    .double-zone {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05); /* 투명 네이비 락커 느낌 */
    }
    
    .kpi-card-zone {
        background: linear-gradient(180deg, var(--bg-card) 0%, #0A1128 100%) !important;
        border-radius: 12px !important;
        padding: 36px 28px 28px 28px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: 4px solid var(--color-gold) !important;
        text-align: center !important;
        margin-bottom: 15px;
        height: 100%;
        position: relative;
    }
    
    .zone-title { color: #A0AEC0 !important; font-weight:700; font-size:1.4rem; margin-bottom:5px; }
    .zone-value { color: var(--color-gold) !important; font-weight:900; font-size:4.0rem; margin:0; }
    .zone-value-sub { color: var(--color-gold) !important; font-weight:900; font-size:2.8rem; margin:0; } /* 너무 크면 카드가 깨지므로 살짝 조정 */
    .unit-text { font-size: 1.2rem; color: #94A3B8; font-weight: 500; }
</style>
'''
st.markdown(double_container_css, unsafe_allow_html=True)

zone_left, spacer, zone_right = st.columns([1, 0.02, 1])

with zone_left:
    st.markdown("<div class='double-zone'>", unsafe_allow_html=True)
    # [좌측 최상단]
    st.markdown(f'''
    <div class="kpi-card-zone">
        <p class="zone-title" style="font-size:1.4rem;">🔵 생명보험 총 수수료</p>
        <h2 class="zone-value">{val_life_new + val_life_ret:,.0f} <span class="unit-text">원</span></h2>
        <p style="color:#A0AEC0; margin-top:5px; font-size:1.1rem;">익월(신계약) + 유지(환수 포함) 수수료 합산</p>
    </div>
    ''', unsafe_allow_html=True)
    
    sub_l1, sub_l2 = st.columns(2)
    with sub_l1:
        st.markdown(f"<div class='kpi-card-zone'><p class='zone-title'>① 생명 익월 수수료</p><h2 class='zone-value-sub'>{val_life_new:,.0f} <span class='unit-text'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(l_new_comp.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_life_new_comp")
        
        if target_scope == '생명 익월' and target_company:
            st.markdown(f"<div class='table-toggle-container'><div class='table-toggle-btn'>[{target_company}] 상품군별 상세 보기</div></div>", unsafe_allow_html=True)
            if len(l_new_prod) > 0:
                disp_dataframe(l_new_prod.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=150, selection_mode="single-row", on_select="rerun", key=f"sel_life_new_prod_{target_company}")
            else:
                st.info("데이터 없음")

    with sub_l2:
        st.markdown(f"<div class='kpi-card-zone'><p class='zone-title'>② 생명 유지(환수포함)</p><h2 class='zone-value-sub'>{val_life_ret:,.0f} <span class='unit-text'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(l_ret_comp.rename(columns={'지사수수료': '유지수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_life_ret_comp")

    st.markdown("</div>", unsafe_allow_html=True)

with zone_right:
    st.markdown("<div class='double-zone'>", unsafe_allow_html=True)
    # [우측 최상단]
    st.markdown(f'''
    <div class="kpi-card-zone">
        <p class="zone-title" style="font-size:1.4rem;">🟠 손해보험 총 수수료</p>
        <h2 class="zone-value">{val_dmg_new + val_dmg_ret + val_dmg_etc:,.0f} <span class="unit-text">원</span></h2>
        <p style="color:#A0AEC0; margin-top:5px; font-size:1.1rem;">익월(신계약) + 유지 + 기타(일반/차/환수) 합산</p>
    </div>
    ''', unsafe_allow_html=True)
    
    sub_r1, sub_r2, sub_r3 = st.columns(3)
    
    with sub_r1:
        st.markdown(f"<div class='kpi-card-zone' style='padding: 24px 10px 10px 10px !important;'><p class='zone-title' style='font-size:1.2rem;'>③ 손해 익월</p><h2 class='zone-value-sub' style='font-size:2.2rem;'>{val_dmg_new:,.0f} <span class='unit-text' style='font-size:1.0rem;'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(d_new_comp.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_dmg_new_comp")
        
        if target_scope == '손해 익월' and target_company:
            st.markdown(f"<div class='table-toggle-container'><div class='table-toggle-btn'>[{target_company[:4]}]</div></div>", unsafe_allow_html=True)
            if len(d_new_prod) > 0:
                disp_dataframe(d_new_prod.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=150, selection_mode="single-row", on_select="rerun", key=f"sel_dmg_new_prod_{target_company}")

    with sub_r2:    
        st.markdown(f"<div class='kpi-card-zone' style='padding: 24px 10px 10px 10px !important;'><p class='zone-title' style='font-size:1.2rem;'>④ 손해 유지</p><h2 class='zone-value-sub' style='font-size:2.2rem;'>{val_dmg_ret:,.0f} <span class='unit-text' style='font-size:1.0rem;'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(d_ret_comp.rename(columns={'지사수수료': '유지수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_dmg_ret_comp")

    with sub_r3:
        st.markdown(f"<div class='kpi-card-zone' style='padding: 24px 10px 10px 10px !important;'><p class='zone-title' style='font-size:1.2rem;'>⑤ 손해 기타</p><h2 class='zone-value-sub' style='font-size:2.2rem;'>{val_dmg_etc:,.0f} <span class='unit-text' style='font-size:1.0rem;'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(d_etc_comp.rename(columns={'지사수수료': '기타수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_dmg_etc_comp")
        
        if target_scope == '손해 기타' and target_company:
            st.markdown(f"<div class='table-toggle-container'><div class='table-toggle-btn'>[{target_company[:4]}]</div></div>", unsafe_allow_html=True)
            if len(d_etc_prod) > 0:
                disp_dataframe(d_etc_prod.rename(columns={'지사수수료': '기타수수료'}), hide_index=True, use_container_width=True, height=150, selection_mode="single-row", on_select="rerun", key=f"sel_dmg_etc_prod_{target_company}")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 10. [최하단] 수수료 전용 상세데이터
"""

start_str = "# ==========================================\n# 9. [하단] 전체 수수료 대시보드 (피라미드 구조)\n# ==========================================\nst.markdown(\"<h3 style='color:#FFFFFF !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #D4AF37;'>💰 전체 수수료 대시보드 (지사수수료 기준)</h3>\", unsafe_allow_html=True)"

end_str = "# ==========================================\n# 10. [최하단] 수수료 전용 상세데이터"

start_idx = text.find(start_str)
end_idx = text.find(end_str)

if start_idx != -1 and end_idx != -1:
    old_section = text[start_idx:end_idx]
    text = text.replace(old_section, new_section_9)
    codecs.open(file_path, "w", "utf-8").write(text)
    print("Dashboard double zone layout applied!")
else:
    print("Could not find section borders.", start_idx, end_idx)
    # let's try regex search
    import re
    match = re.search(r"# ==========================================\n# 9\. \[하단\] 전체 수수료 대시보드.*?# ==========================================\n# 10\. \[최하단\]", text, re.DOTALL)
    if match:
        old_section = match.group(0).replace("# ==========================================\n# 10. [최하단]", "")
        text = text.replace(old_section, new_section_9)
        codecs.open(file_path, "w", "utf-8").write(text)
        print("Dashboard double zone layout applied using regex!")
