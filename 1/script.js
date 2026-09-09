const modal = document.getElementById("modal");

const modalContent =
  document.getElementById("modalContent");


const roleData = {

  writer: {

    title: "Create Your Writer ID",

    sub:
      "Publish your story and turn your manuscript into a real book.",

    steps: [
      "Personal details",
      "Publish type",
      "Book info",
      "Printing",
      "Cover",
      "PDF",
      "Price",
      "Review"
    ]

  },


  printer: {

    title: "Create Your Printer ID",

    sub:
      "Print books on time and help stories reach readers.",

    steps: [
      "Profile",
      "Printing setup",
      "Orders",
      "Printing",
      "Handover",
      "Earnings"
    ]

  },


  reader: {

    title: "Create Your Reader ID",

    sub:
      "Find your next great read and get it delivered to your door.",

    steps: [
      "Account",
      "Discover",
      "Cart",
      "Address",
      "Payment",
      "Tracking",
      "Review"
    ]

  },


  delivery: {

    title: "Create Your Delivery ID",

    sub:
      "Pick up books, deliver them safely and confirm delivery with OTP.",

    steps: [
      "Profile",
      "Documents",
      "Verification",
      "Orders",
      "Pickup",
      "Delivery",
      "OTP"
    ]

  }

};


let currentRole = "";

let currentStep = 0;

let formData = {};



function scrollToRoles() {

  document
    .querySelector("#roles")
    .scrollIntoView({
      behavior: "smooth"
    });

}



function goHome() {

  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });

}



function openModal() {

  modal.classList.add("show");

  modal.setAttribute(
    "aria-hidden",
    "false"
  );

}



function closeModal() {

  modal.classList.remove("show");

  modal.setAttribute(
    "aria-hidden",
    "true"
  );

}



modal.addEventListener(
  "click",
  function (e) {

    if (e.target === modal) {

      closeModal();

    }

  }
);



/* LOGIN */

function openLogin() {

  modalContent.innerHTML = `

    <div class="eyebrow">
      WELCOME BACK
    </div>

    <h2 class="flow-title">
      Sign in to BookConnect
    </h2>

    <p class="flow-sub">
      Choose your role and continue to your dashboard.
    </p>


    <div class="login-tabs">

      <button>
        Writer
      </button>

      <button>
        Printer
      </button>

      <button>
        Reader
      </button>

      <button>
        Delivery
      </button>

    </div>


    <div class="form-grid">

      <div class="field full">

        <label>
          Mobile / Email
        </label>

        <input
          placeholder="Enter mobile number or email"
        >

      </div>


      <div class="field full">

        <label>
          Password
        </label>

        <input
          type="password"
          placeholder="Enter password"
        >

      </div>

    </div>


    <div class="modal-actions">

      <span></span>

      <button
        class="primary-btn"
        onclick="alert('Demo sign-in complete. Connect a backend for real authentication.')">

        Sign in →

      </button>

    </div>

  `;

  openModal();

}



/* START ROLE FLOW */

function startFlow(role) {

  currentRole = role;

  currentStep = 0;

  formData = {};

  renderStep();

  openModal();

}



/* SAVE FORM DATA */

function saveFields() {

  document
    .querySelectorAll("[data-field]")
    .forEach(function (el) {

      formData[el.dataset.field] =
        el.value;

    });


  document
    .querySelectorAll(
      "input[type=radio]:checked"
    )
    .forEach(function (el) {

      formData[el.name] =
        el.value;

    });

}



/* FIELD */

function field(
  label,
  key,
  type = "text",
  full = false,
  placeholder = ""
) {

  return `

    <div class="field ${full ? "full" : ""}">

      <label>
        ${label}
      </label>

      <input
        data-field="${key}"
        type="${type}"
        placeholder="${placeholder}"
      >

    </div>

  `;

}



/* RENDER STEP */

function renderStep() {

  const d =
    roleData[currentRole];


  let body = "";


  if (currentRole === "writer") {

    body = writerStep();

  }


  if (currentRole === "printer") {

    body = printerStep();

  }


  if (currentRole === "reader") {

    body = readerStep();

  }


  if (currentRole === "delivery") {

    body = deliveryStep();

  }


  modalContent.innerHTML = `

    <div class="eyebrow">

      ${currentRole.toUpperCase()}
      · STEP ${currentStep + 1}
      OF ${d.steps.length}

    </div>


    <h2 class="flow-title">

      ${d.title}

    </h2>


    <p class="flow-sub">

      ${d.sub}

    </p>


    <div class="stepbar">

      ${d.steps
        .map(
          (_, i) =>
            `<i class="${
              i <= currentStep
                ? "active"
                : ""
            }"></i>`
        )
        .join("")}

    </div>


    ${body}


    <div class="modal-actions">

      ${
        currentStep > 0

          ? `<button
              class="outline-btn"
              onclick="prevStep()">

              ← Back

            </button>`

          : `<button
              class="outline-btn"
              onclick="closeModal()">

              Cancel

            </button>`
      }


      <button
        class="primary-btn"
        onclick="nextStep()">

        ${
          currentStep ===
          d.steps.length - 1
            ? "Finish"
            : "Continue"
        }

        →

      </button>

    </div>

  `;

}



/* WRITER */

function writerStep() {

  if (currentStep === 0)

    return `

      <div class="form-grid">

        ${field(
          "Full Name *",
          "name",
          "text",
          false,
          "Your full name"
        )}

        ${field(
          "Mobile Number *",
          "number",
          "tel",
          false,
          "10 digit number"
        )}

        ${field(
          "Email",
          "email",
          "email",
          false,
          "you@example.com"
        )}

        ${field(
          "Password *",
          "password",
          "password",
          false,
          "Create password"
        )}

        ${field(
          "Address *",
          "address",
          "text",
          true,
          "Full address"
        )}

        ${field(
          "Bank Account Number",
          "bank",
          "text",
          false,
          "Account number"
        )}

        ${field(
          "IFSC Code",
          "ifsc",
          "text",
          false,
          "IFSC code"
        )}

      </div>

    `;


  if (currentStep === 1)

    return optionGroup(
      "How do you want to publish?",
      [

        [
          "ebook",
          "eBook",
          "Digital edition"
        ],

        [
          "paperback",
          "Paperback Book",
          "Soft-cover physical book"
        ],

        [
          "hardcover",
          "Hardcover Book",
          "Premium hard-cover edition"
        ]

      ]
    );


  if (currentStep === 2)

    return `

      <div class="form-grid">

        <div class="field">

          <label>
            Language *
          </label>

          <select data-field="language">

            <option>
              Hindi
            </option>

            <option>
              English
            </option>

            <option>
              Other
            </option>

          </select>

        </div>


        ${field(
          "Book Title *",
          "title",
          "text",
          false,
          "Enter book title"
        )}


        ${field(
          "Description *",
          "description",
          "text",
          true,
          "Tell readers about your book"
        )}


        ${field(
          "Keywords for Search",
          "keywords",
          "text",
          true,
          "fiction, love, adventure..."
        )}

      </div>

    `;


  if (currentStep === 3)

    return (

      optionGroup(
        "Choose printing options",
        [

          [
            "bw",
            "Black & White",
            "Economical printing"
          ],

          [
            "color",
            "Color",
            "For colorful pages"
          ]

        ]
      )

      +

      `<h3>
        Paper size
      </h3>`

      +

      optionGroup(
        "",
        [

          [
            "5x8",
            "5 × 8 inch",
            "Small size"
          ],

          [
            "6x9",
            "6 × 9 inch",
            "Standard size"
          ],

          [
            "8x12",
            "8 × 12 inch",
            "Large size"
          ]

        ]
      )

    );


  if (currentStep === 4)

    return optionGroup(
      "How will you create your cover?",
      [

        [
          "own",
          "I will create my own cover",
          "Upload your designed cover"
        ],

        [
          "platform",
          "Let platform create it",
          "Design support from BookConnect"
        ]

      ]
    );


  if (currentStep === 5)

    return `

      <div class="field">

        <label>
          Book PDF *
        </label>

        <input
          type="file"
          accept=".pdf"
          data-field="pdf"
        >

      </div>


      <div class="mini-note">

        PDF will be checked for basic
        format and quality.
        ISBN processing can be connected
        to your publishing workflow.

      </div>

    `;


  if (currentStep === 6)

    return `

      <div class="mini-note">

        Suggested price can be calculated
        from page count, size, paper type,
        binding and printing cost.

      </div>


      <div
        class="form-grid"
        style="margin-top:18px">

        ${field(
          "Number of Pages",
          "pages",
          "number",
          false,
          "e.g. 200"
        )}

        ${field(
          "Selling Price (₹)",
          "price",
          "number",
          false,
          "e.g. 250"
        )}

      </div>

    `;


  return `

    <div class="success">

      <div class="check">
        📚
      </div>

      <h2>
        Ready to publish
      </h2>

      <p>
        Review your details and submit
        the book.
      </p>

    </div>

  `;

}



/* PRINTER */

function printerStep() {

  if (currentStep === 0)

    return `

      <div class="form-grid">

        ${field(
          "Full Name *",
          "name",
          "text",
          false,
          "Your full name"
        )}

        ${field(
          "Mobile Number *",
          "number",
          "tel",
          false,
          "Mobile number"
        )}

        ${field(
          "Email",
          "email"
        )}

        ${field(
          "Printing Shop Name",
          "shop"
        )}

        ${field(
          "Address *",
          "address",
          "text",
          true,
          "Shop / work address"
        )}

        ${field(
          "Bank Details",
          "bank",
          "text",
          true,
          "Payment details"
        )}

      </div>

    `;


  if (currentStep === 1)

    return (

      optionGroup(
        "What can you print?",
        [

          [
            "bw",
            "Black & White",
            "Standard printing"
          ],

          [
            "color",
            "Color",
            "Color printing"
          ]

        ]
      )

      +

      `

        <div class="mini-note">

          You can later add supported sizes,
          binding options and printer capacity.

        </div>

      `

    );


  if (currentStep === 2)

    return `

      <div class="status-line">

        <i class="dot current"></i>

        <span>
          3 new book orders available
        </span>

      </div>


      <div class="cart-line">

        <span>
          The Silent Journey · 220 pages
        </span>

        <b>
          12–24 hrs
        </b>

      </div>


      <div class="cart-line">

        <span>
          Mindful Living · 150 pages
        </span>

        <b>
          24 hrs
        </b>

      </div>


      <div class="cart-line">

        <span>
          Tech Simplified · 340 pages
        </span>

        <b>
          24 hrs
        </b>

      </div>

    `;


  if (currentStep === 3)

    return `

      <div class="success">

        <div class="check">
          🖨️
        </div>

        <h2>
          Printing in progress
        </h2>

        <p>
          Print within the required time,
          complete binding and perform
          a quality check.
        </p>

        <div class="mini-note">

          Target: 12–24 hours after
          accepting the order.

        </div>

      </div>

    `;


  if (currentStep === 4)

    return `

      <div class="success">

        <div class="check">
          📦
        </div>

        <h2>
          Ready for handover
        </h2>

        <p>
          Give the completed book to
          the assigned delivery partner
          and confirm the handover.

        </p>

      </div>

    `;


  return `

    <div class="success">

      <div class="check">
        ⭐
      </div>

      <h2>
        Your printer dashboard
      </h2>

      <p>
        Completed orders, earnings,
        ratings, reviews and tips
        can appear here.
      </p>

    </div>

  `;

}



/* READER */

function readerStep() {

  if (currentStep === 0)

    return `

      <div class="form-grid">

        ${field(
          "User Name *",
          "username"
        )}

        ${field(
          "Full Name *",
          "name"
        )}

        ${field(
          "Mobile Number *",
          "number",
          "tel"
        )}

        ${field(
          "Email",
          "email"
        )}

        ${field(
          "Password *",
          "password"
        )}

      </div>

    `;


  if (currentStep === 1)

    return `

      <div class="field full">

        <label>
          Search books
        </label>

        <input
          data-field="search"
          placeholder="Search by title, author or keyword"
        >

      </div>


      <div class="mini-note">

        Example:
        The Silent Journey · ₹250 ·
        Paperback · 4.5★

      </div>

    `;


  if (currentStep === 2)

    return `

      <div class="cart-line">

        <span>
          The Silent Journey × 1
        </span>

        <b>
          ₹250
        </b>

      </div>


      <div class="cart-line">

        <span>
          Mindful Living × 1
        </span>

        <b>
          ₹300
        </b>

      </div>


      <h3>
        Total: ₹550
      </h3>

    `;


  if (currentStep === 3)

    return `

      <div class="form-grid">

        ${field(
          "Full Name *",
          "addressName"
        )}

        ${field(
          "Mobile Number *",
          "addressNumber",
          "tel"
        )}

        ${field(
          "House / Flat No. *",
          "house"
        )}

        ${field(
          "Street / Area *",
          "street"
        )}

        ${field(
          "City *",
          "city"
        )}

        ${field(
          "State *",
          "state"
        )}

        ${field(
          "PIN Code *",
          "pin"
        )}

      </div>

    `;


  if (currentStep === 4)

    return (

      optionGroup(
        "Choose payment method",
        [

          [
            "cod",
            "Cash on Delivery",
            "Pay when the book arrives"
          ],

          [
            "online",
            "Pay Online",
            "UPI, card, net banking"
          ]

        ]
      )

      +

      field(
        "PAN / KYC details (if required)",
        "pan",
        "text",
        true,
        "Only when applicable"
      )

    );


  if (currentStep === 5)

    return `

      <div class="status-line">

        <i class="dot done"></i>

        <span>
          Order placed
        </span>

      </div>


      <div class="status-line">

        <i class="dot done"></i>

        <span>
          Printer assigned
        </span>

      </div>


      <div class="status-line">

        <i class="dot done"></i>

        <span>
          Printing in progress
        </span>

      </div>


      <div class="status-line">

        <i class="dot current"></i>

        <span>
          Out for delivery
        </span>

      </div>


      <div class="status-line">

        <i class="dot"></i>

        <span>
          Delivered
        </span>

      </div>

    `;


  return `

    <div class="success">

      <div class="check">
        ⭐
      </div>

      <h2>
        Rate your book
      </h2>

      <p>
        Give 1–5 stars and write
        a review after receiving
        your order.
      </p>


      <div class="option-grid">

        <label class="option selected">

          <b>
            ★★★★★
          </b>

          <small>
            Excellent
          </small>

        </label>


        <label class="option">

          <b>
            ★★★★☆
          </b>

          <small>
            Good
          </small>

        </label>


        <label class="option">

          <b>
            ★★★☆☆
          </b>

          <small>
            Okay
          </small>

        </label>

      </div>


      ${field(
        "Your review",
        "review",
        "text",
        true,
        "Write your experience..."
      )}

    </div>

  `;

}



/* DELIVERY BOY */

function deliveryStep() {

  if (currentStep === 0)

    return `

      <div class="form-grid">

        ${field(
          "Full Name *",
          "name"
        )}

        ${field(
          "Mobile Number *",
          "number",
          "tel"
        )}

        ${field(
          "Email",
          "email"
        )}

        ${field(
          "Address *",
          "address",
          "text",
          true
        )}

        ${field(
          "Vehicle Type *",
          "vehicle"
        )}

        ${field(
          "Vehicle Number *",
          "vehicleNo"
        )}

      </div>

    `;


  if (currentStep === 1)

    return `

      <div class="form-grid">

        ${field(
          "Driving Licence *",
          "license",
          "file"
        )}

        ${field(
          "Vehicle RC *",
          "rc",
          "file"
        )}

        ${field(
          "Vehicle Insurance",
          "insurance",
          "file"
        )}

      </div>


      <div class="mini-note">

        Upload the required documents
        for verification before taking
        delivery orders.

      </div>

    `;


  if (currentStep === 2)

    return `

      <div class="success">

        <div class="check">
          🔍
        </div>

        <h2>
          Verification status
        </h2>

        <p>
          Your documents are under review.
        </p>


        <div class="status-line">

          <i class="dot done"></i>

          <span>
            Documents submitted
          </span>

        </div>


        <div class="status-line">

          <i class="dot current"></i>

          <span>
            Under verification
          </span>

        </div>


        <div class="status-line">

          <i class="dot"></i>

          <span>
            Approved
          </span>

        </div>

      </div>

    `;


  if (currentStep === 3)

    return `

      <div class="cart-line">

        <span>
          #BC1021 · The Silent Journey
        </span>

        <b>
          ₹40
        </b>

      </div>


      <div class="cart-line">

        <span>
          #BC1022 · Mindful Living
        </span>

        <b>
          ₹35
        </b>

      </div>


      <div class="mini-note">

        Accept an available order
        to start the pickup process.

      </div>

    `;


  if (currentStep === 4)

    return `

      <div class="success">

        <div class="check">
          📦
        </div>

        <h2>
          Pick up from printer
        </h2>

        <p>
          Collect the correct number
          of copies and confirm pickup
          in the app.
        </p>

      </div>

    `;


  if (currentStep === 5)

    return `

      <div class="success">

        <div class="check">
          🛵
        </div>

        <h2>
          Out for delivery
        </h2>

        <p>
          Navigate to the reader's
          saved address and deliver
          the book safely.
        </p>

      </div>

    `;


  return `

    <div class="success">

      <div class="check">
        🔐
      </div>

      <h2>
        OTP confirmation
      </h2>

      <p>
        Ask the reader for the
        delivery OTP and enter it
        to complete the order.
      </p>


      <div class="form-grid">

        ${field(
          "Delivery OTP",
          "otp",
          "text",
          true,
          "Enter 6-digit OTP"
        )}

      </div>

    </div>

  `;

}



/* OPTION GROUP */

function optionGroup(
  title,
  options
) {

  return `

    <h3>
      ${title}
    </h3>


    <div class="option-grid">

      ${options
        .map(
          function (o) {

            return `

              <label class="option">

                <input
                  type="radio"
                  name="option"
                  value="${o[0]}"
                  onchange="selectOption(this)"
                >


                <b>
                  ${o[1]}
                </b>


                <small>
                  ${o[2]}
                </small>

              </label>

            `;

          }
        )
        .join("")}

    </div>

  `;

}



/* SELECT OPTION */

function selectOption(input) {

  input
    .closest(".option-grid")
    .querySelectorAll(".option")
    .forEach(
      function (x) {

        x.classList.remove(
          "selected"
        );

      }
    );


  input
    .closest(".option")
    .classList.add(
      "selected"
    );

}



/* NEXT */

function nextStep() {

  saveFields();


  if (
    currentStep <
    roleData[currentRole].steps.length - 1
  ) {

    currentStep++;

    renderStep();

  }

  else {

    modalContent.innerHTML = `

      <div class="success">

        <div class="check">
          ✓
        </div>

        <h2>
          Demo setup complete!
        </h2>

        <p>
          Your ${currentRole}
          journey has been completed
          in this front-end prototype.
        </p>


        <div class="mini-note">

          <b>
            Next:
          </b>

          connect a backend/database,
          authentication, payment gateway,
          file storage, OTP service and
          real order tracking.

        </div>


        <div class="modal-actions">

          <span></span>

          <button
            class="primary-btn"
            onclick="closeModal()">

            Back to BookConnect

          </button>

        </div>

      </div>

    `;

  }

}



/* BACK */

function prevStep() {

  saveFields();


  if (currentStep > 0) {

    currentStep--;

    renderStep();

  }

}



/* ESC KEY */

document.addEventListener(
  "keydown",
  function (e) {

    if (e.key === "Escape") {

      closeModal();

    }

  }
);