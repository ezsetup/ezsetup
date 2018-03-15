ALTER TABLE public.labs ADD COLUMN IF NOT EXISTS error_msgs TEXT[] DEFAULT array[]::TEXT[];
