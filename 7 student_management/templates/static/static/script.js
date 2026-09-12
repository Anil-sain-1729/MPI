function searchStudent() {

    let input =
        document.getElementById("search");

    let filter =
        input.value.toLowerCase();

    let rows =
        document.querySelectorAll(
            "#studentTable tbody tr"
        );


    rows.forEach(function(row) {

        let text =
            row.innerText.toLowerCase();


        if (text.includes(filter)) {

            row.style.display = "";

        }

        else {

            row.style.display = "none";

        }

    });

}