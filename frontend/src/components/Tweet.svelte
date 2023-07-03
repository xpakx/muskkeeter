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
    import LinkCard from "./LinkCard.svelte";
    import QuotedTweet from "./QuotedTweet.svelte";
    export let tweet: TweetDetails;

    const formatter = new Intl.DateTimeFormat("default", {
        month: "short",
        day: "numeric",
    });

    const long_formatter = new Intl.DateTimeFormat("default", {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: false,
    });
</script>

<div class="tweet">
    <div class="avatar">
        <img src={tweet.author.avatar} alt="avatar" />
    </div>
    <div class="tweet-column">
        <div class="header">
            {#if tweet.retweeted}
                <div class="retweet-header">
                    <Fa icon={faReply} /> retweeted
                </div>
            {/if}
            <div class="user-header">
                <div class="user-data">
                    <div class="user-data_name">{tweet.author.name}</div>
                    <div class="user-data_handle">
                        <a href="/{tweet.author.username}" rel="external">
                            @{tweet.author.username}
                        </a>
                    </div>
                </div>
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

        {#if tweet.images}
            <div class="images">
                {#each tweet.images as img}
                    <img src={img} alt="img" />
                {/each}
            </div>
        {/if}

        {#if tweet.link}
            <LinkCard link={tweet.link} />
        {/if}

        {#if tweet.quoted}
            <QuotedTweet tweet={tweet.quoted} />
        {/if}

        <div class="date">
            {long_formatter.format(tweet.date)}
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

    .user-data_handle a,
    .date-header a {
        color: #f2cdcd;
        text-decoration: none;
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

    .images img {
        max-width: 200px;
    }

    .retweet-header {
        font-size: 13px;
        color: #a6adc8;
    }
</style>
