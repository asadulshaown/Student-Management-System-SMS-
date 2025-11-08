

document.addEventListener('DOMContentLoaded', () => {
    const semesterSelect = document.getElementById('semester');
    const tableBody = document.getElementById('table_body');
    const studentId = semesterSelect.dataset.studentId;      

    semesterSelect.addEventListener('change', function() {
        const semesterId = this.value;
        const studentId = this.value;
        fetch(`/get_student_results/?student_id=${studentId}&semester_id=${semesterId}`)
            .then(response => response.json())
            .then(data => {
                tableBody.innerHTML = ''; 

                if (data.results && data.results.length > 0) {
                    data.results.forEach(res => {
                        let row = `
                            <tr>
                                <td></td>
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
                            
                            <td colspan="7" class="text-center text-danger">No results found for this semester.</td>
                        </tr>
                        `;
                }
            })
            .catch(error => {
                console.error("Error fetching results:", error);
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="7" class="text-center text-danger">Error loading data.</td>
                    </tr>
                `;
            });
    });
});
