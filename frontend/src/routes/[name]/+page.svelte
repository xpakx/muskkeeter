<script lang="ts">
    import { page } from "$app/stores";
    import Tweet from "../../components/Tweet.svelte";
    import type { TweetDetails } from "../../types/tweet";
    let name = $page.params.name;
    let apiUri = "http://localhost:8000";
    let message: String;
    let tweets: TweetDetails[] = [];
    getTimeline(name);
    const TIMELINE = 0;
    const REPLIES = 1;
    let active_card = TIMELINE;

    async function getTimeline(username: String) {
        try {
            let response = await fetch(`${apiUri}/profile/${username}`, {
                method: "GET",
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                for (let tweet of fromEndpoint) {
                    tweet.date = new Date(tweet.date);
                }
                tweets = fromEndpoint;
            } else {
                const errorBody = await response.json();
                message = errorBody.detail;
            }
        } catch (err) {
            if (err instanceof Error) {
                message = err.message;
            }
        }
    }

    async function getReplies(username: String) {
        try {
            let response = await fetch(
                `${apiUri}/profile/${username}/replies`,
                {
                    method: "GET",
                }
            );

            if (response.ok) {
                let fromEndpoint = await response.json();
                for (let tweet of fromEndpoint) {
                    tweet.date = new Date(tweet.date);
                }
                tweets = fromEndpoint;
            } else {
                const errorBody = await response.json();
                message = errorBody.detail;
            }
        } catch (err) {
            if (err instanceof Error) {
                message = err.message;
            }
        }
    }

    async function loadTimeline() {
        if (active_card == TIMELINE) {
            return;
        }
        active_card = TIMELINE;
        getTimeline(name);
    }

    async function loadReplies() {
        if (active_card == REPLIES) {
            return;
        }
        active_card = REPLIES;
        getReplies(name);
    }
</script>

<svelte:head>
    <title>{name}</title>
</svelte:head>

<h1>{name}'s profile</h1>
<div class="cards">
    <button on:click={loadTimeline}>Tweets</button>
    <button on:click={loadReplies}>Tweets & replies</button>
</div>

{#each tweets as tweet}
    <Tweet {tweet} />
{/each}

<style>
</style>
