<script lang="ts">
    import { page } from "$app/stores";
    import Tweet from "../../components/Tweet.svelte";
    import type { TweetDetails } from "../../types/tweet";
    let name = $page.params.name;
    let apiUri = "http://localhost:8000";
    let message: String;
    let tweets: TweetDetails[] = [];
    getTimer(name);

    async function getTimer(username: String) {
        try {
            let response = await fetch(`${apiUri}/profile/${username}`, {
                method: "GET",
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                for(let tweet of fromEndpoint) {
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
</script>

<svelte:head>
    <title>{name}</title>
</svelte:head>

<h1>{name}'s profile</h1>
{#each tweets as tweet}
   <Tweet {tweet} /> 
{/each}

<style>
</style>
