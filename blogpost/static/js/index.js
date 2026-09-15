const postsContainer = document.getElementById("posts-container");
const paginationContainer = document.querySelector(".pagination");

const API_BASE = "/0.1/posts/";
const PAGE_SIZE = 2;

let currentApiUrl = API_BASE;


// ------------------------------------
// تبدیل URL API به URL داخلی سایت
// ------------------------------------
function normalizeApiUrl(url) {
    if (!url) {
        return null;
    }

    const parsedUrl = new URL(url, window.location.origin);

    return parsedUrl.pathname + parsedUrl.search;
}


// ------------------------------------
// دریافت اطلاعات API
// ------------------------------------
async function loadPosts(url = API_BASE) {
    try {
        const apiUrl = normalizeApiUrl(url);

        const response = await fetch(apiUrl, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        console.log("API DATA:", data);

        const posts = data.results;

        console.log("DataSet: ", this.dataset);
        // ------------------------------------
        // پاک کردن پست‌های قبلی
        // ------------------------------------
        postsContainer.innerHTML = "";


        // ------------------------------------
        // اگر پستی وجود نداشت
        // ------------------------------------
        if (!posts || posts.length === 0) {

            postsContainer.innerHTML = `
                <div class="container mt-5 p-4 shadow-lg">
                    <p class="text-muted">
                        هنوز پستی وجود ندارد.
                    </p>
                </div>
            `;

            paginationContainer.innerHTML = "";

            return;
        }


        // ------------------------------------
        // نمایش پست‌ها
        // ------------------------------------
        posts.forEach(post => {

            const description = post.description || "";

            const shortDescription =
                description.length > 200
                    ? description.substring(0, 200) + "..."
                    : description;


            const likesCount =
                Array.isArray(post.likes)
                    ? post.likes.length
                    : 0;


            postsContainer.innerHTML += `
                <div class="container mt-5 p-4 shadow-lg">

                    <h2>
                        <a
                            href="/detail/${post.id}/"
                            class="text-decoration-none text-info"
                        >
                            ${post.title}
                        </a>
                    </h2>

                    <hr>

                    <p>
                        ${shortDescription}

                        <a
                            href="/detail/${post.id}/"
                            class="text-decoration-none text-info"
                        >
                            <span>
                                مطالعه بیشتر
                            </span>
                        </a>
                    </p>

                    <hr>

                    <h6 class="text-muted small">
                        نویسنده:
                        ${post.author}
                    </h6>

                    <h6 class="text-muted small">
                        🧡
                        ${likesCount}
                    </h6>

                </div>
            `;
        });


        // ------------------------------------
        // ذخیره صفحه فعلی
        // ------------------------------------
        currentApiUrl = apiUrl;


        // ------------------------------------
        // ساخت Pagination
        // ------------------------------------
        buildPagination(data);

    } catch (error) {

        console.error("API ERROR:", error);

        postsContainer.innerHTML = `
            <div class="container mt-5 p-4 shadow-lg">
                <p class="text-danger">
                    خطا در دریافت اطلاعات
                </p>
            </div>
        `;

        paginationContainer.innerHTML = "";
    }
}


// ------------------------------------
// ساخت Pagination
// ------------------------------------
function buildPagination(data) {

    paginationContainer.innerHTML = "";


    // اگر API صفحه‌بندی نشده باشد
    if (
        !data ||
        Array.isArray(data) ||
        data.count === undefined
    ) {
        return;
    }


    // ------------------------------------
    // شماره صفحه فعلی
    // ------------------------------------
    const currentUrl =
        new URL(
            currentApiUrl,
            window.location.origin
        );

    const currentPage =
        parseInt(
            currentUrl.searchParams.get("page") || "1",
            10
        );


    // ------------------------------------
    // تعداد کل صفحات
    // ------------------------------------
    const totalPages =
        Math.ceil(data.total_pages);

    // ------------------------------------
    // شماره صفحات
    // ------------------------------------
    for (
        let page = 1;
        page <= totalPages;
        page++
    ) {

        if (
            page === 1 ||
            page === totalPages ||
            Math.abs(page - currentPage) <= 2
        ) {

            const pageUrl =
                `${API_BASE}?page=${page}`;


            paginationContainer.innerHTML += `
                <li
                    class="page-item
                    ${page === currentPage ? "active" : ""}"
                >

                    <a
                        href="?page=${page}"
                        class="page-link"
                        id="page-link"

                        data-url="${pageUrl}"
                        onclick="
                            loadPosts(this.dataset.url);
                            return false;
                        "
                    >
                        ${page}
                    </a>

                </li>
            `;
        }
    }

}


// ------------------------------------
// اجرای اولیه
// ------------------------------------
loadPosts();
