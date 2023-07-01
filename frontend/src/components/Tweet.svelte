<script lang="ts">
    import type { TweetDetails } from "../types/tweet";

    export let tweet: TweetDetails;


    const formatter = new Intl.DateTimeFormat("default", {
        month: "short",
        day: "numeric",
    });
</script>

<div class="tweet">
    <div class="avatar">
        <img src={tweet.author.avatar} alt="avatar" />
    </div>
    <div class="tweet-column">
        <div class="header">
            {#if tweet.retweeted}
            <div class="retweet-header">retweeted</div>
            {/if}
            <div class="user-header">
                <div class="user-data">
                    <div class="user-data_name">{tweet.author.name}</div>
                    <div class="user-data_handle">@{tweet.author.username}</div>
                </div>
                <div class="date">{tweet.date}</div>
            </div>
            </div>
        <div class="content">
            {tweet.text}
        </div>

        <div class="date">
            {tweet.date}
        </div>
        <div class="actions">
            <span>{tweet.replies}</span>
            <span>{tweet.retweets}</span>
            <span>{tweet.quotes}</span>
            <span>{tweet.favs}</span>
        </div>
    </div>
</div>

<style>
    .tweet {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
    }

    .avatar img {
        border-radius: 50%;
    }

    .tweet-column {
        flex-grow: 1;
    }

    .header, .content {
        margin-bottom: 10px;
    }

    .user-header {
        display: flex;
        justify-content: space-between;
    }

    .user-data {
        display: flex;
        gap: 5px;
    }

    .user-data_name {
        font-weight: bold;
        color: #a6adc8; 
    }
    
    .user-data_handle {
        color: #f2cdcd;
    }

    .date, .actions {
        font-size: 13px;
    }

    .actions {
        font-weight: bold;
    }
</style>