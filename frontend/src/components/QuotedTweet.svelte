<script lang="ts">
    import Fa from "svelte-fa/src/fa.svelte";
    import type { Quote } from "../types/quote";
    export let tweet: Quote;

    const formatter = new Intl.DateTimeFormat("default", {
        month: "short",
        day: "numeric",
    });
</script>

<div class="tweet">
    <div class="tweet-column">
        <div class="header">
            <div class="user-header">
                <div class="avatar">
                    <img src={tweet.author.avatar} alt="avatar" />
                </div>
                <div class="user-data">
                    <div class="user-data_name">{tweet.author.name}</div>
                    <div class="user-data_handle">
                        <a href="/{tweet.author.username}" rel="external">
                            @{tweet.author.username}
                        </a>
                    </div>
                </div>
                <span class="separator">·</span>
                <div class="date-header">
                    <a
                        href="/{tweet.author.username}/status/{tweet.id}"
                        rel="external"
                    >
                        {formatter.format(tweet.date)}
                    </a>
                </div>
            </div>
        </div>
        <div class="content">
            {tweet.text}
        </div>
    </div>
</div>

<style>
    .tweet {
        margin-bottom: 15px;
        border-radius: 5px;
        border: 1px solid #a6adc8;
    }

    .avatar img {
        border-radius: 50%;
        width: 20px;
        height: 20px;
    }

    .tweet-column {
        flex-grow: 1;
    }

    .header {
        margin-bottom: 10px;
    }

    .content {
        margin-bottom: 5px;
    }

    .user-header {
        display: flex;
    }

    .user-data {
        display: flex;
        gap: 5px;
    }

    .user-data_name {
        font-weight: bold;
        color: #a6adc8;
    }

    .user-data_handle a,
    .date-header a {
        color: #f2cdcd;
        text-decoration: none;
    }

    .user-header .separator {
        margin: 0 5px;
    }
</style>
