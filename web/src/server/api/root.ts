import { createTRPCRouter } from "~/server/api/trpc";
import { mandateRouter } from "~/server/api/routers/mandate";
import { agentRouter } from "~/server/api/routers/agent";

/**
 * This is the primary router for your server.
 *
 * All routers added in /api/routers should be manually added here.
 */
export const appRouter = createTRPCRouter({
  mandate: mandateRouter,
  agent: agentRouter,
});

// export type definition of API
export type AppRouter = typeof appRouter;
