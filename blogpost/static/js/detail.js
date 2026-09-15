/*
==========================================
اطلاعات کاربر فعلی
==========================================
*/

/*
==========================================
گرفتن ID پست از URL
مثال:
/detail/5/
==========================================
*/
const pathParts = window.location.pathname
    .split("/")
    .filter(Boolean);
const postId =
    pathParts[pathParts.length - 1];
/*
==========================================
DOM
==========================================
*/
const postContainer =
    document.getElementById("post-container");
const commentsContainer =
    document.getElementById("comments-container");
/*
==========================================
دریافت پست
==========================================
*/
async function loadPost() {
    try {
        const response = await fetch(
            `/0.1/post/${postId}/`,
            {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json"
                }
            }
        );
        if (!response.ok) {
            throw new Error(
                "خطا در دریافت اطلاعات پست"
            );
        }
        const post =
            await response.json();
        console.log("POST:", post);
        /*
        ==========================================
        تعداد لایک
        ==========================================
        */
        const likesCount =
            Array.isArray(post.likes)
                ? post.likes.length
                : 0;
        /*
        ==========================================
        بررسی اینکه کاربر فعلی لایک کرده یا نه
        ==========================================
        */
        const userLiked =
            isAuthenticated &&
            Array.isArray(post.likes) &&
            post.likes.includes(currentUsername);
        /*
        ==========================================
        تصویر
        ==========================================
        */
        let pictureHTML = "";
        if (post.picture) {
            pictureHTML = `
                <img
                    src="${post.picture}"
                    alt="${post.title}"
                    class="img-fluid"
                >
                <hr>
            `;
        }
        /*
        ==========================================
        لایک
        ==========================================
        */
        let likeHTML = "";
        if (isAuthenticated) {
            likeHTML = `
                <form
                    action=""
                    method="post"
                >
                    <input
                        type="hidden"
                        name="csrfmiddlewaretoken"
                        value="${getCSRFToken()}"
                    >
                    <h6 class="text-muted small">
                        <button
                            class="btn ${
                                userLiked
                                    ? "btn-success"
                                    : "btn-outline-success"
                            }"
                            type="submit"
                            name="action"
                            value="like"
                        >
                            🧡 ${likesCount}
                        </button>
                    </h6>
                </form>
            `;
        } else {
            likeHTML = `
                <h6 class="text-muted small">
                    🧡 ${likesCount}
                </h6>
            `;
        }
        /*
        ==========================================
        ویرایش / حذف
        ==========================================
        */
        let authorActions = "";
        if (
            isAuthenticated &&
            currentUsername === post.author
        ) {
            authorActions = `
                <a
                    class="btn btn-outline-warning m-3"
                    href="/update/${post.id}/"
                >
                    ویرایش پست
                </a>
                <a
                    class="btn btn-outline-danger m-3"
                    href="/delete/${post.id}/"
                >
                    حذف پست
                </a>
            `;
        }
        /*
        ==========================================
        تاریخ‌ها
        ==========================================
        */
        let datesHTML = "";
        if (post.datetime_created) {
            datesHTML += `
                <h6 class="text-muted small">
                    تاریخ ایجاد:
                    ${formatDate(post.datetime_created)}
                </h6>
            `;
        }
        if (post.datetime_modified) {
            datesHTML += `
                <h6 class="text-muted small">
                    تاریخ آخرین ویرایش:
                    ${formatDate(post.datetime_modified)}
                </h6>
            `;
        }
        /*
        ==========================================
        ساخت پست
        ==========================================
        */
        postContainer.innerHTML = `
            <h1>
                <a
                    href="#"
                    class="text-decoration-none text-info"
                >
                    ${escapeHTML(post.title)}
                </a>
            </h1>
            <hr>
            ${pictureHTML}
            <p>
                ${escapeHTML(post.description)}
            </p>
            <hr>
            <h6 class="text-muted small">
                نویسنده:
                ${escapeHTML(post.author)}
            </h6>
            ${datesHTML}
            ${likeHTML}
            ${authorActions}
        `;
        /*
        ==========================================
        کامنت‌ها
        ==========================================
        */
        renderComments(post.comments);
    } catch (error) {
        console.error(error);
        postContainer.innerHTML = `
            <div class="alert alert-danger">
                دریافت اطلاعات پست با خطا مواجه شد.
            </div>
        `;
        commentsContainer.innerHTML = "";
    }
}
/*
==========================================
نمایش کامنت‌ها
==========================================
*/
function renderComments(comments) {
    if (
        !comments ||
        comments.length === 0
    ) {
        commentsContainer.innerHTML = `
            <h4 class="mt-4">
                اولین نفری باشید که
                برای این پست کامنت می‌گذارد.
            </h4>
        `;
        return;
    }
    commentsContainer.innerHTML = "";
    comments.forEach(comment => {
        let nameHTML = "";
        if (comment.hide_name) {
            nameHTML = `
                <h4 class="mt-4">
                    شخص ناشناسی گفته:
                </h4>
            `;
        } else {
            nameHTML = `
                <h4 class="mt-4">
                    ${escapeHTML(comment.name)}
                    گفته:
                </h4>
            `;
        }
        commentsContainer.innerHTML += `
            ${nameHTML}
            <p>
                ${escapeHTML(comment.comment)}
            </p>
            <hr>
        `;
    });
}
/*
==========================================
CSRF
==========================================
*/
function getCSRFToken() {
    const csrfInput =
        document.querySelector(
            "[name=csrfmiddlewaretoken]"
        );
    if (csrfInput) {
        return csrfInput.value;
    }
    return "";
}
/*
==========================================
تاریخ
==========================================
*/
function formatDate(dateString) {
    const date =
        new Date(dateString);
    return date.toLocaleString(
        "fa-IR",
        {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}
/*
==========================================
جلوگیری از HTML Injection
==========================================
*/
function escapeHTML(value) {
    if (value === null || value === undefined) {
        return "";
    }
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
/*
==========================================
اجرای API
==========================================
*/
loadPost();