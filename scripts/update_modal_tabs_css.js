const fs = require('fs');

let styleCss = fs.readFileSync('dashboard/style.css', 'utf8');

const enhancedModalCss = `/* ==========================================================================
   MODAL WINDOWS (CRIMSON GLASS) & RESPONSIVE TABS BAR
   ========================================================================== */

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(8, 1, 3, 0.88);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-card {
  background: rgba(20, 6, 11, 0.96);
  border: 1px solid var(--border-dark);
  border-radius: 12px;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.8), 0 0 35px rgba(229, 9, 46, 0.3);
  max-width: 1250px;
  width: 95vw;
  max-height: 90vh;
  height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: modal-pop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modal-pop {
  from { transform: scale(0.96); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-header {
  padding: 14px 20px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(32, 8, 16, 0.95);
  flex-shrink: 0;
}

.modal-header-nav {
  display: flex;
  align-items: center;
  gap: 14px;
}

.modal-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-subtitle {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 3px;
}

.modal-tabs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  background: rgba(18, 4, 9, 0.98);
  border-bottom: 1px solid var(--border-color);
  padding: 8px 16px;
  gap: 6px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 30;
}

.tab-btn {
  background: rgba(28, 6, 14, 0.7);
  border: 1px solid rgba(229, 9, 46, 0.25);
  border-radius: 6px;
  color: var(--text-silver);
  padding: 6px 12px;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.tab-btn:hover {
  color: #ffffff;
  background: rgba(229, 9, 46, 0.25);
  border-color: #fef08a;
  transform: translateY(-1px);
  box-shadow: 0 0 10px rgba(254, 240, 138, 0.3);
}

.tab-btn.active {
  color: #ffffff;
  border-color: var(--crimson-ruby);
  background: linear-gradient(135deg, rgba(229, 9, 46, 0.45), rgba(122, 12, 26, 0.65));
  box-shadow: 0 0 14px rgba(229, 9, 46, 0.45);
  font-weight: 700;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.tab-pane {
  display: none;
}
.tab-pane.active {
  display: block;
}`;

// Replace modal windows section in style.css
const startModalSec = "/* ==========================================================================\n   MODAL WINDOWS (CRIMSON GLASS)";
const endModalSec = "/* ==========================================================================\n   SIH GRAND FINALE STYLES";

const sIdx = styleCss.indexOf(startModalSec);
const eIdx = styleCss.indexOf(endModalSec);

if (sIdx !== -1 && eIdx !== -1) {
  styleCss = styleCss.substring(0, sIdx) + enhancedModalCss + "\n\n" + styleCss.substring(eIdx);
  fs.writeFileSync('dashboard/style.css', styleCss, 'utf8');
  console.log('Successfully replaced modal section in style.css');
} else {
  console.log('Could not find modal section indices:', sIdx, eIdx);
}
