/**
 * TaskFlow — Main JavaScript
 * Handles: sidebar toggle, task toggle (AJAX), delete modal, search auto-submit
 */

/* ── DOM Ready ──────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initSidebar();
  initSearch();
  initFlashAutoDismiss();
});

/* ── Sidebar Toggle (mobile) ─────────────────────────────────── */
function initSidebar() {
  const toggle  = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (!toggle || !sidebar) return;

  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
  });

  overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
  });
}

/* ── Toggle Task Status via AJAX ─────────────────────────────── */
async function toggleTask(taskId, btn) {
  try {
    const res  = await fetch(`/toggle/${taskId}`, { method: 'POST' });
    if (!res.ok) throw new Error('Request failed');
    const data = await res.json();

    const card  = document.getElementById(`task-${taskId}`);
    const icon  = btn.querySelector('i');
    const isDone = data.status === 'Completed';

    // Update button appearance
    btn.classList.toggle('checked', isDone);
    icon.className = isDone ? 'bi bi-check-lg' : 'bi bi-circle';

    // Update card styling
    card.classList.toggle('task-done', isDone);

    // Update status dot text
    const statusDot = card.querySelector('.status-dot');
    if (statusDot) {
      statusDot.className = `meta-item status-dot status-${data.status.toLowerCase()}`;
      statusDot.innerHTML = `<i class="bi bi-circle-fill"></i> ${data.status}`;
    }

    showToast(isDone ? 'Task completed! 🎉' : 'Task marked as pending.', isDone ? 'success' : 'info');

  } catch (err) {
    console.error('Toggle failed:', err);
    showToast('Could not update task. Please refresh.', 'error');
  }
}

/* ── Delete Confirm Modal ────────────────────────────────────── */
function confirmDelete(taskId, taskTitle) {
  const modal     = document.getElementById('deleteModal');
  const nameLabel = document.getElementById('deleteTaskName');
  const form      = document.getElementById('deleteForm');

  nameLabel.textContent = `"${taskTitle}" will be permanently removed.`;
  form.action = `/delete/${taskId}`;

  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
}

/* ── Search Auto-submit on Enter ─────────────────────────────── */
function initSearch() {
  const searchInput = document.querySelector('.search-input');
  if (!searchInput) return;

  let debounceTimer;
  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      searchInput.closest('form').submit();
    }, 500);
  });
}

/* ── Toast Notification ──────────────────────────────────────── */
function showToast(message, type = 'success') {
  const existing = document.querySelector('.tf-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = `tf-toast tf-toast-${type}`;
  toast.innerHTML = `
    <i class="bi ${type === 'success' ? 'bi-check-circle-fill' : type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-info-circle-fill'}"></i>
    <span>${message}</span>
  `;

  // Inline styles for the toast (no extra CSS needed)
  Object.assign(toast.style, {
    position:     'fixed',
    bottom:       '24px',
    right:        '24px',
    background:   type === 'success' ? 'rgba(52,211,153,0.15)' : type === 'error' ? 'rgba(248,113,113,0.15)' : 'rgba(96,165,250,0.15)',
    border:       `1px solid ${type === 'success' ? 'rgba(52,211,153,0.3)' : type === 'error' ? 'rgba(248,113,113,0.3)' : 'rgba(96,165,250,0.3)'}`,
    color:        type === 'success' ? '#34d399' : type === 'error' ? '#f87171' : '#60a5fa',
    padding:      '12px 18px',
    borderRadius: '10px',
    display:      'flex',
    alignItems:   'center',
    gap:          '8px',
    fontSize:     '0.85rem',
    fontWeight:   '500',
    fontFamily:   "'DM Sans', sans-serif",
    zIndex:       '9999',
    backdropFilter: 'blur(12px)',
    animation:    'toastIn 0.25s ease',
    boxShadow:    '0 8px 24px rgba(0,0,0,0.4)',
  });

  // Inject keyframes if not already present
  if (!document.getElementById('toastKeyframes')) {
    const style = document.createElement('style');
    style.id = 'toastKeyframes';
    style.textContent = `
      @keyframes toastIn  { from { opacity:0; transform: translateY(10px); } to { opacity:1; transform: translateY(0); } }
      @keyframes toastOut { from { opacity:1; } to { opacity:0; transform: translateY(10px); } }
    `;
    document.head.appendChild(style);
  }

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'toastOut 0.25s ease forwards';
    setTimeout(() => toast.remove(), 260);
  }, 2800);
}

/* ── Flash Auto-dismiss ──────────────────────────────────────── */
function initFlashAutoDismiss() {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach((flash, i) => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.4s ease';
      flash.style.opacity = '0';
      setTimeout(() => flash.remove(), 400);
    }, 4000 + i * 300);
  });
}
