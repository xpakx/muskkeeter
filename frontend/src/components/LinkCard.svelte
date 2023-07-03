<script lang="ts">
    import type { Link } from "../types/link";
    export let link: Link;
</script>

<div class="link_card">
    <div class="image">
        <img src={link.image} alt="avatar" />
    </div>
    <div class="link-column">
        <div class="link-data">
            <div class="domain">
                {link.domain}
            </div>
            <div class="title">
                {link.title}
            </div>
            <div class="description">
                {link.description}
            </div>
        </div>
    </div>
</div>

<style>
    .link_card {
        display: flex;
        gap: 10px;
        border-radius: 5px;
        border: 1px solid #a6adc8;
        overflow: hidden;
    }

    .link-column {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
    }

    .domain,
    .description {
        color: #a6adc8;
    }
</style>
