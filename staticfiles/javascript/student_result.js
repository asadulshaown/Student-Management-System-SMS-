
document.addEventListener('DOMContentLoaded', () => {
    const semesterSelect = document.getElementById('semester');
    const tableBody = document.getElementById('table_body');

    // find student_id from url
    const pathParts = window.location.pathname.split('/');
    const student_id = pathParts[2]; 

    semesterSelect.addEventListener('change', async function() {
        const semesterId = this.value;
        tableBody.innerHTML = "<h4>Loading.....</h4>";

        try {
            // Fetch request
            const response = await fetch(`/get_student_results/?student_id=${student_id}&semester_id=${semesterId}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // Table update
            tableBody.innerHTML = ''; 
            if (data.results && data.results.length > 0) {
                data.results.forEach((res, index) => {
                    const row = `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${res.exam}</td>
                            <td>${res.subject}</td>
                            <td>${res.code}</td>
                            <td>${res.marks}</td>
                            <td>${res.grade}</td>
                            <td>${res.cgpa}</td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });
            } else {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="7" class="text-center text-danger">
                            No results found for this semester.
                        </td>
                    </tr>
                `;
            }

        } catch (error) {
            console.error("Error fetching results:", error);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-danger">Error loading data.</td>
                </tr>
            `;
        }
    });
});
