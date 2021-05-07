<template>
    <header>
        <h3>Know your parliament</h3>
    </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
    setup() {
        return {}
    },
})
</script>

<style lang="scss" scoped>
    header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: var(--header-height);
        backdrop-filter: blur('8px');
        padding: 0 var(--gutter-width);
        display: flex;
        align-items: center;
    }
</style>