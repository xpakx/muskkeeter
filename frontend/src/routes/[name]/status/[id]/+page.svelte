<script lang="ts">
    import { page } from "$app/stores";
    import Tweet from "../../../../components/Tweet.svelte";
    import type { TweetDetails } from "../../../../types/tweet";
    let name = $page.params.name;
    let id = $page.params.id;
    let apiUri = "http://localhost:8000";
    let message: String;
    let tweet: TweetDetails | undefined = undefined;
    getTweet(id);

    async function getTweet(id: String) {
        try {
            let response = await fetch(`${apiUri}/tweet/${id}`, {
                method: "GET",
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                fromEndpoint.date = new Date(fromEndpoint.date);
                tweet = fromEndpoint;
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

{#if tweet}
    <Tweet {tweet} />
{/if}

<style>
</style>
