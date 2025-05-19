const reportList = document.getElementById('reportList');
const reportContent = document.getElementById('reportContent');
const searchInput = document.getElementById('searchInput');
const sortSelect = document.getElementById('sortSelect');

let reports = [];

async function loadReports() {
  try {
    const res = await fetch('files.json');
    reports = await res.json();
    displayReports();
  } catch (e) {
    reportList.innerHTML = '<p>Error loading report list.</p>';
  }
}

function displayReports() {
  const query = searchInput.value.toLowerCase();
  let filtered = reports.filter(r =>
    r.unit_name.toLowerCase().includes(query) ||
    r.audit_year.toString().includes(query)
  );

  if (sortSelect.value === 'year') {
    filtered.sort((a, b) => a.audit_year - b.audit_year);
  } else {
    filtered.sort((a, b) => a.unit_name.localeCompare(b.unit_name));
  }

  reportList.innerHTML = '';
  if (filtered.length === 0) {
    reportList.innerHTML = '<p>No reports found.</p>';
    reportContent.innerHTML = '<p>Select a report to view details here.</p>';
    return;
  }

  filtered.forEach(report => {
    const div = document.createElement('div');
    div.className = 'report-item';
    div.textContent = `${report.unit_name} (${report.audit_year}) - Observations: ${report.observations_count}`;
    div.onclick = () => loadReportContent(report.filename);
    reportList.appendChild(div);
  });
}

async function loadReportContent(filename) {
  try {
    const res = await fetch(`data/${filename}`);
    if (!res.ok) throw new Error('File not found');
    const md = await res.text();
    reportContent.innerHTML = marked.parse(md);
  } catch (e) {
    reportContent.innerHTML = `<p>Error loading report content.</p>`;
  }
}

searchInput.addEventListener('input', displayReports);
sortSelect.addEventListener('change', displayReports);

loadReports();
