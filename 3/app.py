from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>BookConnect</title>


    <style>

        * {
            box-sizing: border-box;
        }


        body {

            margin: 0;

            font-family:
                Arial,
                sans-serif;

            background: #fbfaf7;

            color: #211d1b;

        }


        /* NAVBAR */

        nav {

            height: 75px;

            padding: 0 7%;

            background: white;

            display: flex;

            align-items: center;

            justify-content: space-between;

            border-bottom:
                1px solid #eee;

            position: sticky;

            top: 0;

            z-index: 10;

        }


        .logo {

            font-size: 25px;

            font-weight: bold;

            color: #9e2735;

        }


        nav button {

            background: white;

            color: #9e2735;

            border: 1px solid #9e2735;

            padding: 10px 20px;

            border-radius: 8px;

            cursor: pointer;

        }


        /* HERO */

        .hero {

            min-height: 600px;

            padding: 80px 8%;

            display: flex;

            align-items: center;

            justify-content: space-between;

            gap: 50px;

            background:
                linear-gradient(
                    135deg,
                    #fff8f1,
                    #f5e8df
                );

        }


        .hero-text {

            max-width: 600px;

        }


        .small-title {

            color: #9e2735;

            font-size: 13px;

            letter-spacing: 2px;

            font-weight: bold;

        }


        h1 {

            font-size: 75px;

            line-height: 1;

            margin: 20px 0;

        }


        h1 span {

            color: #9e2735;

        }


        .hero p {

            font-size: 18px;

            line-height: 1.7;

            color: #6d6660;

        }


        .start-btn {

            margin-top: 25px;

            background: #9e2735;

            color: white;

            border: none;

            padding: 15px 25px;

            border-radius: 9px;

            font-size: 16px;

            font-weight: bold;

            cursor: pointer;

        }


        /* BOOK IMAGE */

        .books {

            width: 350px;

            height: 350px;

            position: relative;

        }


        .book {

            position: absolute;

            width: 250px;

            height: 150px;

            border-radius: 8px;

            display: flex;

            justify-content: center;

            align-items: center;

            color: white;

            font-size: 25px;

            font-weight: bold;

            box-shadow:
                0 20px 40px
                rgba(0,0,0,.15);

        }


        .book1 {

            background: #9e2735;

            top: 50px;

            left: 50px;

            transform: rotate(-8deg);

        }


        .book2 {

            background: #315c68;

            top: 120px;

            left: 80px;

            transform: rotate(7deg);

        }


        .book3 {

            background: #d09a52;

            top: 190px;

            left: 30px;

            transform: rotate(-3deg);

        }


        /* ROLES */

        .roles {

            padding: 90px 7%;

            text-align: center;

        }


        .roles h2 {

            font-size: 42px;

        }


        .role-container {

            display: grid;

            grid-template-columns:
                repeat(4, 1fr);

            gap: 20px;

            margin-top: 45px;

        }


        .role {

            background: white;

            padding: 30px 20px;

            border-radius: 18px;

            border:
                1px solid #eee;

            transition: .3s;

        }


        .role:hover {

            transform:
                translateY(-8px);

            box-shadow:
                0 15px 40px
                rgba(0,0,0,.1);

        }


        .role-icon {

            font-size: 50px;

        }


        .role h3 {

            font-size: 26px;

        }


        .role p {

            color: #777;

            line-height: 1.5;

            min-height: 65px;

        }


        .role button {

            border: none;

            color: white;

            padding: 12px 18px;

            border-radius: 8px;

            cursor: pointer;

            font-weight: bold;

        }


        .writer button {

            background: #9e2735;

        }


        .printer button {

            background: #245b92;

        }


        .reader button {

            background: #28734c;

        }


        .delivery button {

            background: #b57916;

        }


        /* HOW IT WORKS */

        .how {

            padding: 90px 7%;

            background: #f5eee7;

            text-align: center;

        }


        .steps {

            display: grid;

            grid-template-columns:
                repeat(4,1fr);

            gap: 20px;

            margin-top: 40px;

        }


        .step {

            background: white;

            padding: 25px;

            border-radius: 15px;

            text-align: left;

        }


        .step-number {

            color: #9e2735;

            font-weight: bold;

        }


        .step h3 {

            margin-top: 15px;

        }


        .step p {

            color: #777;

        }


        /* FOOTER */

        footer {

            background: #211d1b;

            color: white;

            text-align: center;

            padding: 30px;

        }


        /* MODAL */

        .modal {

            position: fixed;

            inset: 0;

            background:
                rgba(0,0,0,.65);

            display: none;

            align-items: center;

            justify-content: center;

            padding: 20px;

            z-index: 100;

        }


        .modal.active {

            display: flex;

        }


        .modal-box {

            background: white;

            width: 500px;

            max-width: 100%;

            padding: 35px;

            border-radius: 20px;

            position: relative;

        }


        .close {

            position: absolute;

            right: 20px;

            top: 15px;

            border: none;

            background: #eee;

            width: 35px;

            height: 35px;

            border-radius: 50%;

            font-size: 22px;

            cursor: pointer;

        }


        .modal-box h2 {

            color: #9e2735;

            font-size: 32px;

        }


        .form-group {

            margin-bottom: 15px;

        }


        .form-group label {

            display: block;

            font-weight: bold;

            margin-bottom: 6px;

        }


        .form-group input {

            width: 100%;

            padding: 12px;

            border:
                1px solid #ddd;

            border-radius: 8px;

        }


        .continue {

            width: 100%;

            background: #9e2735;

            color: white;

            border: none;

            padding: 13px;

            border-radius: 8px;

            cursor: pointer;

            font-weight: bold;

        }


        /* MOBILE */

        @media(max-width: 900px) {

            .hero {

                flex-direction: column;

                text-align: center;

            }


            .role-container {

                grid-template-columns:
                    repeat(2,1fr);

            }


            .steps {

                grid-template-columns:
                    repeat(2,1fr);

            }

        }


        @media(max-width: 600px) {

            h1 {

                font-size: 50px;

            }


            .role-container,
            .steps {

                grid-template-columns: 1fr;

            }


            .books {

                transform: scale(.8);

            }

        }

    </style>

</head>


<body>


<!-- NAVBAR -->

<nav>

    <div class="logo">

        📖 BookConnect

    </div>


    <button onclick="openLogin()">

        Sign In

    </button>

</nav>



<!-- HERO -->

<section class="hero">


    <div class="hero-text">

        <div class="small-title">

            WRITE · PRINT · READ · DELIVER

        </div>


        <h1>

            Books connect
            <span>people.</span>

        </h1>


        <p>

            A platform where writers publish,
            printers create books, delivery
            partners move them and readers
            discover their next story.

        </p>


        <button
            class="start-btn"
            onclick="goRoles()">

            Get Started →

        </button>

    </div>



    <div class="books">

        <div class="book book1">

            WRITE

        </div>


        <div class="book book2">

            READ

        </div>


        <div class="book book3">

            CONNECT

        </div>

    </div>


</section>



<!-- ROLES -->

<section
    class="roles"
    id="roles">

    <div class="small-title">

        CHOOSE YOUR ROLE

    </div>


    <h2>

        Be part of the book journey.

    </h2>


    <p>

        Choose how you want to use
        BookConnect.

    </p>


    <div class="role-container">


        <!-- WRITER -->

        <div class="role writer">

            <div class="role-icon">

                ✍️

            </div>


            <h3>

                Writer

            </h3>


            <p>

                Publish your book as
                eBook, paperback or
                hardcover.

            </p>


            <button
                onclick="openRole('Writer')">

                Join as Writer →

            </button>

        </div>



        <!-- PRINTER -->

        <div class="role printer">

            <div class="role-icon">

                🖨️

            </div>


            <h3>

                Printer

            </h3>


            <p>

                Receive book orders,
                print them and hand
                them to delivery.

            </p>


            <button
                onclick="openRole('Printer')">

                Join as Printer →

            </button>

        </div>



        <!-- READER -->

        <div class="role reader">

            <div class="role-icon">

                📚

            </div>


            <h3>

                Reader

            </h3>


            <p>

                Discover books,
                order them and
                review them.

            </p>


            <button
                onclick="openRole('Reader')">

                Join as Reader →

            </button>

        </div>



        <!-- DELIVERY -->

        <div class="role delivery">

            <div class="role-icon">

                🛵

            </div>


            <h3>

                Delivery Boy

            </h3>


            <p>

                Pick up books and
                safely deliver them
                to readers.

            </p>


            <button
                onclick="openRole('Delivery Boy')">

                Join as Delivery →

            </button>

        </div>


    </div>

</section>



<!-- HOW IT WORKS -->

<section class="how">

    <div class="small-title">

        HOW IT WORKS

    </div>


    <h2>

        From manuscript to doorstep.

    </h2>


    <div class="steps">


        <div class="step">

            <div class="step-number">
                01
            </div>

            <h3>
                ✍️ Writer
            </h3>

            <p>
                Writer publishes the
                book and uploads PDF.
            </p>

        </div>


        <div class="step">

            <div class="step-number">
                02
            </div>

            <h3>
                🖨️ Printer
            </h3>

            <p>
                Printer receives the
                order and prints it.
            </p>

        </div>


        <div class="step">

            <div class="step-number">
                03
            </div>

            <h3>
                🛵 Delivery
            </h3>

            <p>
                Delivery partner picks
                up and delivers the book.
            </p>

        </div>


        <div class="step">

            <div class="step-number">
                04
            </div>

            <h3>
                📖 Reader
            </h3>

            <p>
                Reader receives the book
                and gives a review.
            </p>

        </div>


    </div>

</section>



<!-- FOOTER -->

<footer>

    <h3>
        📖 BookConnect
    </h3>

    <p>
        Stories travel. People connect.
    </p>

</footer>



<!-- MODAL -->

<div
    class="modal"
    id="modal">


    <div class="modal-box">


        <button
            class="close"
            onclick="closeModal()">

            ×

        </button>


        <h2 id="modalTitle">

            Create Your ID

        </h2>


        <p>

            Enter your details to
            continue with BookConnect.

        </p>


        <div class="form-group">

            <label>
                Name
            </label>

            <input
                id="name"
                placeholder="Enter your name">

        </div>


        <div class="form-group">

            <label>
                Mobile Number
            </label>

            <input
                id="number"
                placeholder="Enter mobile number">

        </div>


        <div class="form-group">

            <label>
                Email
            </label>

            <input
                id="email"
                placeholder="Enter email">

        </div>


        <div class="form-group">

            <label>
                Address
            </label>

            <input
                id="address"
                placeholder="Enter address">

        </div>


        <button
            class="continue"
            onclick="createAccount()">

            Create ID →

        </button>


    </div>

</div>



<script>

    function goRoles() {

        document
            .getElementById("roles")
            .scrollIntoView({
                behavior: "smooth"
            });

    }


    function openRole(role) {

        document
            .getElementById("modalTitle")
            .innerText =
            "Create Your " +
            role +
            " ID";

        document
            .getElementById("modal")
            .classList
            .add("active");

    }


    function openLogin() {

        document
            .getElementById("modalTitle")
            .innerText =
            "Sign In to BookConnect";

        document
            .getElementById("modal")
            .classList
            .add("active");

    }


    function closeModal() {

        document
            .getElementById("modal")
            .classList
            .remove("active");

    }


    function createAccount() {

        let name =
            document
            .getElementById("name")
            .value;


        let number =
            document
            .getElementById("number")
            .value;


        if (
            name === "" ||
            number === ""
        ) {

            alert(
                "Please enter your name and mobile number."
            );

            return;

        }


        alert(
            "Welcome to BookConnect, "
            + name
            + "!"
        );


        closeModal();

    }


    window.onclick = function(event) {

        let modal =
            document.getElementById("modal");


        if (event.target === modal) {

            closeModal();

        }

    };

</script>


</body>

</html>
"""


@app.route("/")
def home():

    return render_template_string(HTML)


if __name__ == "__main__":

    app.run(
        debug=True
    )