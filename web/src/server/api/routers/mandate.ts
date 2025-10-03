import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";

/**
 * Mandate router - communicates with FastAPI backend
 */
export const mandateRouter = createTRPCRouter({
  getUserMandates: publicProcedure
    .input(z.object({ userId: z.string() }))
    .query(async ({ input }) => {
      // TODO: Call FastAPI backend at /api/v1/mandates/user/{user_id}
      // For now, return mock data
      return {
        mandates: [],
        message: `Fetching mandates for user: ${input.userId}`,
      };
    }),

  getMandate: publicProcedure
    .input(z.object({ mandateId: z.string() }))
    .query(async ({ input }) => {
      // TODO: Call FastAPI backend at /api/v1/mandates/{id}
      return {
        mandate: null,
        message: `Fetching mandate: ${input.mandateId}`,
      };
    }),
});
