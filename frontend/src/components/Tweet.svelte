<script lang="ts">
    import type { TweetDetails } from "../types/tweet";
    import Fa from "svelte-fa/src/fa.svelte";
    import {
        faHeart,
        faMessage,
        faQuoteRight,
        faReply,
        faReplyAll,
    } from "@fortawesome/free-solid-svg-icons";
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
                <div class="retweet-header"><Fa icon={faReply} /> retweeted</div>
            {/if}
            <div class="user-header">
                <div class="user-data">
                    <div class="user-data_name">{tweet.author.name}</div>
                    <div class="user-data_handle">@{tweet.author.username}</div>
                </div>
                <div class="date-header">{tweet.date}</div>
            </div>
        </div>
        <div class="content">
            {tweet.text}
        </div>

        <div class="date">
            {tweet.date}
        </div>
        <div class="actions">
            <span><Fa icon={faMessage} /> {tweet.replies}</span>
            <span><Fa icon={faReplyAll} /> {tweet.retweets}</span>
            <span><Fa icon={faQuoteRight} /> {tweet.quotes}</span>
            <span><Fa icon={faHeart} /> {tweet.favs}</span>
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

    .header {
        margin-bottom: 10px;
    }

    .content {
        margin-bottom: 5px;
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

    .actions {
        font-size: 13px;
        font-weight: bold;
        display: flex;
        gap: 5px;
    }

    .date {
        font-size: 13px;
        margin-bottom: 5px;
    }
</style>
