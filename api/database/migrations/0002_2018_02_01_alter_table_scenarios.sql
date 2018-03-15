ALTER TABLE public.scenarios ADD COLUMN IF NOT EXISTS sg_rules TEXT[] DEFAULT array[]::TEXT[];
