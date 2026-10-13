/**
 * AttendEase — Interactive Client Script
 * Handles mobile navigation, dynamic modals, attendance marking toggles,
 * bulk actions, table search, and Chart.js visualizations.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Sidebar Toggle
    const mobileToggleBtn = document.getElementById('mobileToggleBtn');
    const appSidebar = document.getElementById('appSidebar');

    if (mobileToggleBtn && appSidebar) {
        mobileToggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            appSidebar.classList.toggle('show-sidebar');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 992 && 
                !appSidebar.contains(e.target) && 
                !mobileToggleBtn.contains(e.target)) {
                appSidebar.classList.remove('show-sidebar');
            }
        });
    }

    // 2. Generic Modal Helpers
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    };

    // Close modal on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-backdrop-custom').forEach(modal => {
                if (modal.style.display === 'flex') {
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
            });
        }
    });

    // Close modal when clicking backdrop
    document.querySelectorAll('.modal-backdrop-custom').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    });

    // 3. Interactive Attendance Marking Sheet Logic
    const attendanceForm = document.getElementById('attendanceMarkingForm');
    if (attendanceForm) {
        const rows = document.querySelectorAll('.att-student-row');
        
        function updateAttendanceSummary() {
            let presentCount = 0;
            let absentCount = 0;
            let leaveCount = 0;

            rows.forEach(row => {
                const sid = row.getAttribute('data-student-id');
                const input = document.getElementById(`status_input_${sid}`);
                if (input) {
                    if (input.value === 'present') presentCount++;
                    else if (input.value === 'absent') absentCount++;
                    else if (input.value === 'leave') leaveCount++;
                }
            });

            const presentBadge = document.getElementById('countPresent');
            const absentBadge = document.getElementById('countAbsent');
            const leaveBadge = document.getElementById('countLeave');

            if (presentBadge) presentBadge.textContent = presentCount;
            if (absentBadge) absentBadge.textContent = absentCount;
            if (leaveBadge) leaveBadge.textContent = leaveCount;
        }

        window.setStudentStatus = function(studentId, status) {
            const input = document.getElementById(`status_input_${studentId}`);
            if (!input) return;

            input.value = status;
            const container = document.getElementById(`status_btns_${studentId}`);
            if (container) {
                container.querySelectorAll('.att-status-btn').forEach(btn => {
                    btn.classList.remove('selected-present', 'selected-absent', 'selected-leave');
                });

                const activeBtn = container.querySelector(`[data-status="${status}"]`);
                if (activeBtn) {
                    activeBtn.classList.add(`selected-${status}`);
                }
            }
            updateAttendanceSummary();
        };

        window.markAllStudents = function(status) {
            rows.forEach(row => {
                const sid = row.getAttribute('data-student-id');
                window.setStudentStatus(sid, status);
            });
        };

        // Initial summary computation
        updateAttendanceSummary();
    }

    // 4. Client-side Real-time Search Filter for Tables
    const quickSearchInput = document.getElementById('tableQuickSearch');
    if (quickSearchInput) {
        quickSearchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            const tableRows = document.querySelectorAll('.filterable-table tbody tr');
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }

    // 5. Chart.js Initializations
    initDashboardCharts();
});

function initDashboardCharts() {
    // Check if Chart.js is available
    if (typeof Chart === 'undefined') return;

    // Monthly Trend Chart
    const trendCtx = document.getElementById('attendanceTrendChart');
    if (trendCtx && window.dashboardChartData) {
        const d = window.dashboardChartData;
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: d.trend_labels || [],
                datasets: [{
                    label: 'Overall Attendance Rate (%)',
                    data: d.trend_values || [],
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: '#4f46e5',
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: { callback: v => v + '%' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Department Distribution Chart
    const deptCtx = document.getElementById('deptDistributionChart');
    if (deptCtx && window.dashboardChartData) {
        const d = window.dashboardChartData;
        new Chart(deptCtx, {
            type: 'bar',
            data: {
                labels: d.dept_labels || [],
                datasets: [
                    {
                        label: 'Students',
                        data: d.dept_students || [],
                        backgroundColor: '#3b82f6',
                        borderRadius: 6
                    },
                    {
                        label: 'Faculty',
                        data: d.dept_faculty || [],
                        backgroundColor: '#8b5cf6',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' }
                }
            }
        });
    }

    // Faculty Section Performance Chart
    const facultyCtx = document.getElementById('facultySectionsChart');
    if (facultyCtx && window.dashboardChartData) {
        const d = window.dashboardChartData;
        new Chart(facultyCtx, {
            type: 'bar',
            data: {
                labels: d.section_labels || [],
                datasets: [{
                    label: 'Average Attendance (%)',
                    data: d.section_values || [],
                    backgroundColor: d.section_values.map(v => v < 75 ? '#ef4444' : '#10b981'),
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: { callback: v => v + '%' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Student Course Breakdown Chart
    const studentCtx = document.getElementById('studentCoursesChart');
    if (studentCtx && window.dashboardChartData) {
        const d = window.dashboardChartData;
        new Chart(studentCtx, {
            type: 'bar',
            data: {
                labels: d.course_labels || [],
                datasets: [{
                    label: 'My Attendance (%)',
                    data: d.course_values || [],
                    backgroundColor: d.course_values.map(v => v < 75 ? '#ef4444' : '#4f46e5'),
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: { callback: v => v + '%' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
}
