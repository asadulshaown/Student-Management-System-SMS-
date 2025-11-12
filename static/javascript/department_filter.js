
document.addEventListener('DOMContentLoaded', () => {
  const deptSelect = document.getElementById('deptSelect');
  const studentList = document.getElementById('studentList');

  deptSelect.addEventListener('change', async () => {
    const deptId = deptSelect.value;
    studentList.innerHTML = "<h4>Loading...</h4>";

    try {
      // Fetch data using async/await
      const response = await fetch(`/admin/EMS/department/filter-students/?dept_id=${deptId}`);

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      studentList.innerHTML = "";

      if (data.length > 0) {
        data.forEach((stu, index) => {
          const row = `
            <tr>
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
        studentList.innerHTML = "<tr><td colspan='5'>No students found.</td></tr>";
      }

    } catch (error) {
      console.error("Fetch error:", error);
      studentList.innerHTML = "<tr><td colspan='5'>Error loading data.</td></tr>";
    }
  });
});
