
document.addEventListener('DOMContentLoaded', () => {
  const deptSelect = document.getElementById('deptSelect');
  const studentList = document.getElementById('studentList');

  deptSelect.addEventListener('change', () => {
    const deptId = deptSelect.value;
    studentList.innerHTML = "<h4>Loading...</h4>";

    fetch(`/admin/EMS/department/filter-students/?dept_id=${deptId}`)
      .then(response => response.json())
      .then(data => {
        studentList.innerHTML = "";
        if (data.length > 0) {
          data.forEach(stu => {
            let row = ` <tr>
                            <td>${index + 1}</td>
                            <td>${stu.student_name}</td>
                            <td>${stu.roll}</td>
                            <td>${stu.district}</td>
                            <td>${stu.student_phone_number}</td>
                        </tr>
                        `;
                        studentList.innerHTML += row;
                     
          });
        } else {
          studentList.innerHTML = "<li>No students found.</li>";
        }
      })
      .catch(err => {
        console.error("Fetch error:", err);
        studentList.innerHTML = "<li>Error loading data.</li>";
      });
  });
});

console.log('hi');
