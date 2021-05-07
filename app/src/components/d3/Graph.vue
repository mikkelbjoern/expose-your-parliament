<template>
    <svg
        class="d3-graph"
        ref="svg"
        :width="width"
        :height="height"
        :viewBox="`0, 0, ${width}, ${height}`"
    >
        <line v-for="link in graph.links" :key="link.index"
            :x1="link.source.x"
            :y1="link.source.y"
            :x2="link.target.x"
            :y2="link.target.y"
            stroke="black"
            :stroke-width="Math.sqrt(link.value)"
        />

        <circle v-for="node in graph.nodes" :key="node.index"
            :cx="node.x"
            :cy="node.y"
            :r="8"
            :fill="color(node) || colors[Math.ceil(Math.sqrt(node.index))]"
            stroke="white"
            stroke-width="1"
            v-tooltip="node.id"
        />

    </svg>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, PropType, reactive, ref } from 'vue'

import * as d3 from 'd3'
import { d3Types } from '@/components/d3/types'
import { tooltip } from '@/services/tooltip.service'

const scale = d3.scaleOrdinal(d3.schemeCategory10);
const color = (node: d3Types.d3Node) => {
    return scale(node.group.toString())
}

type GraphNode<N> = d3.SimulationNodeDatum & N
type GraphLink<N,L> = d3.SimulationLinkDatum<GraphNode<N>> & L
interface Graph<N,L> {
    simulation: d3.Simulation<GraphNode<N>,GraphLink<N,L>> | null;
    nodes: GraphNode<N>[];
    links: GraphLink<N,L>[];
}

export default defineComponent({
  props: {
        data: {
            type: Object as PropType<d3Types.d3Graph>,
            required: true
        },
        height: { default: 600 },
        width: { default: 600 }
  },
  setup(props) {
    const svg = ref<SVGSVGElement | null>(null)
    const graph = reactive<Graph<d3Types.d3Node, d3Types.d3Link>>({
        simulation: null,
        nodes: [],
        links: []
    })

    onMounted(() => {          
        setTimeout(() => {
            createGraph()
        }, 750)
    })

    onUnmounted(() => {
        graph.simulation?.stop()
    })

    function createGraph () {
        graph.nodes = props.data.nodes.map(d => Object.create(d))
        graph.links = props.data.links.map(d => Object.create(d))

        d3.forceLink(graph.links).distance(d => 100)

        graph.simulation = d3.forceSimulation(graph.nodes)
            .force("link", d3.forceLink(graph.links)
                .distance(d => 40)
                .id((d: any) => d.id))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(props.width / 2, props.height / 2));
                        
        setTimeout(() => {
            d3.select(svg.value)
                .selectAll<SVGCircleElement, unknown>('circle')
                .call(d3.drag<SVGCircleElement, unknown>()
                    .on("start", onDragStart)
                    .on("drag", onDrag)
                    .on("end", onDragEnd))
        }, 1000)
    }

    let draggedNode: GraphNode<d3Types.d3Node> | undefined | null = null 

    function onDragStart (event: any) { 
        if (!event.active) graph.simulation?.alphaTarget(0.3).restart();
        graph.simulation?.velocityDecay(0.2)
        const draggedIndex = graph.simulation?.find(event.subject.x, event.subject.y)?.index        
        draggedNode = draggedIndex != undefined ? graph.simulation?.nodes()[draggedIndex]: null
    }
    function onDrag (event: any) {
        if (draggedNode) {
            draggedNode.fx = event.x
            draggedNode.fy = event.y 
        }     
        tooltip().hide()
    }
    function onDragEnd (event: any) {
        if (!event.active) graph.simulation?.alphaTarget(0);
        if (draggedNode) {
            draggedNode.fx = null
            draggedNode.fy = null
        }
        tooltip().show()
    }

    return { svg, graph, color }
  },
})
</script>

<style lang="scss" scoped>
.d3-graph {
    line {
        stroke: var(--color-1);
        stroke-opacity: 0.3;
    }
    circle {
        //fill: var(--color-5);
    }
}
</style>