import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";

/**
 * Agent router - communicates with FastAPI backend
 */
export const agentRouter = createTRPCRouter({
  getUserAgents: publicProcedure
    .input(z.object({ userId: z.string() }))
    .query(async ({ input }) => {
      // TODO: Call FastAPI backend at /api/v1/agents/user/{user_id}
      return {
        agents: [],
        message: `Fetching agents for user: ${input.userId}`,
      };
    }),

  getAgent: publicProcedure
    .input(z.object({ agentId: z.string() }))
    .query(async ({ input }) => {
      // TODO: Call FastAPI backend at /api/v1/agents/{id}
      return {
        agent: null,
        message: `Fetching agent: ${input.agentId}`,
      };
    }),

  getAgentPerformance: publicProcedure
    .input(z.object({ agentId: z.string() }))
    .query(async ({ input }) => {
      // TODO: Call FastAPI backend for agent performance metrics
      return {
        performance: {
          totalTrades: 0,
          successRate: 0,
          totalReturn: 0,
        },
        message: `Fetching performance for agent: ${input.agentId}`,
      };
    }),
});
