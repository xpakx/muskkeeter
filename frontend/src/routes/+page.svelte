<script type="ts">
    import { goto } from "$app/navigation";

    let name = "";


    function login() {
        if (name != "") {
            goto(`/${name}`)
        }
    }
</script>

<div class="main-container">
    <div class="search-bar">
        <form class="search-form">
            <input
                type="text"
                placeholder="Enter username..."
                id="username"
                bind:value={name}
            />
            <button type="submit" on:click={login}>go</button>
        </form>
    </div>
</div>

<style>
    .main-container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }

    .search-bar {
        margin: 0;
    }

    form.search-form {
        padding: 12px;
        border-radius: 4px;
        display: flex;
        background: #181825;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
        margin: auto;
        margin-top: auto;
        margin-top: -50px;
    }

    form.search-form input {
        font-size: 16px;
        width: 100%;
        background: #1e1e2e;
        color: #cdd6f4;
        border: 0;
        border-radius: 4px;
        padding: 4px;
        margin-right: 8px;
    }

    form.search-form button {
        background: #1e1e2e;
        color: #cdd6f4;
        border: 0;
        border-radius: 3px;
        cursor: pointer;
        font-weight: bold;
    }
</style>
