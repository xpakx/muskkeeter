<script lang="ts">
    import { page } from "$app/stores";
    let name = $page.params.name;
    let apiUri = "http://localhost:8000";
    let message: String;
    let tweets: {id: number, text: String}[] = [];
    getTimer(name);

    async function getTimer(username: String) {
        try {
            let response = await fetch(`${apiUri}/profile/${username}`, {
                method: "GET",
            });

            if (response.ok) {
                tweets = await response.json();
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
<div class="tweet">{tweet.text}</div>
    
{/each}

<style>
</style>
