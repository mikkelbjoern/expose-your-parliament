<template>
    <svg
        class="d3-scatter"
        ref="svg"
        :width="width"
        :height="height"
        :viewBox="`0, 0, ${width}, ${height}`"
    >
        <g :fill="color">
            <rect v-for="(bin, i) in chart.bins" :key="i"
                :x="x(bin.x0) + 1"
                :width="Math.max(0, x(bin.x1) - x(bin.x0) - 1)"
                :y="y(bin.length)"
                :height="y.range()[0] - y(bin.length)"
                :title="0"
                v-tooltip="`${bin.x0}-${bin.x1}`"
            />
        </g>
        
        <g fill="currentColor">
            <text class="d3-histogram-title" :transform="`translate(${width/2},${20})`"> {{ title }} </text>
            <text class="d3-histogram-xlabel" :transform="`translate(${width/2},${height - 5})`"> {{ xlabel }} </text>
            <text class="d3-histogram-ylabel" :transform="`translate(${20},${height/2}) rotate(-90)`" > {{ ylabel }} </text>
        </g>

    </svg>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, PropType, reactive, ref } from 'vue'

import * as d3 from 'd3'
import { d3Types } from '@/components/d3/types'

const margin = {top: 30, right: 20, bottom: 40, left: 50}

export default defineComponent({
  props: {
        data: {
            type: Object as PropType<number[]>,
            required: true
        },
        height: { default: 300 },
        width: { default: 600 },
        bins: { default: 10 },
        color: { default: 'var(--color-1)' },
        title: { default: 'Title' },
        xlabel: { default: 'X-label' },
        ylabel: { default: 'Y-label' },
        xlog: { default: false },
        ylog: { default: false }
  },
  setup(props) {
    const svg = ref<SVGSVGElement | null>(null)
    const chart = reactive<{
        bins: d3.Bin<number,number>[];
    }>({
        bins: []
    })    

    const { x, y } = createChart() 

    function createChart () {
        const data = props.xlog ? props.data.map(d => Math.log(d)) : props.data
        chart.bins = d3.bin().thresholds(props.bins)(data)

        if (props.ylog) {
            chart.bins = chart.bins.filter(bin => bin.length !== 0)
        }

        const x = d3.scaleLinear()
            .domain([Number(chart.bins[0].x0), Number(chart.bins[chart.bins.length - 1].x1)])
            .range([margin.left, props.width - margin.right])
        const y = (props.ylog ? d3.scaleLog() : d3.scaleLinear())
            .domain([0 + (props.ylog ? 0.001 : 0), d3.max(chart.bins, d => d.length) || 1]).nice()
            .range([props.height - margin.bottom, margin.top])

        setTimeout(() => {
            svg.value && d3.select(svg.value).append("g").call(xAxis)
            svg.value && d3.select(svg.value).append("g").call(yAxis)
        }, 100)

        return { x, y }
    }
    
    function xAxis (g: d3.Selection<SVGGElement, unknown, null, undefined>) {
        g.attr("transform", `translate(0,${props.height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(props.width / 80 ).tickSizeOuter(0))
    }

    function yAxis (g: d3.Selection<SVGGElement, unknown, null, undefined>) {
        g.attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(props.height / 40))
    }

    return { svg, chart, x, y, margin }
  },
})
</script>

<style lang="scss" scoped>
.d3-scatter {
    text-anchor: middle;
    &-title {
        font-size: 1.5rem;
        font-family: 'Knewave', cursive;
        text-transform: uppercase;
    }
    &-xlabel, &-ylabel {
        font-size: .75rem;
    }
}
</style>