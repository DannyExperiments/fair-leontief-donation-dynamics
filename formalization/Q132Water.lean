import Std
namespace WaterFill
abbrev Row := Rat × Rat × Rat
/-- A row gives outside donations, the valuation, and the alternative donation. -/
def need (t : Rat) (r : Row) := max 0 (t*r.2.1-r.1)
def budget (f : Row → Rat) : List Row → Rat
  | [] => 0
  | r :: rest => f r + budget f rest
/-- At the water level t, every nonnegative feasible alternative allocates
at least the shortfall in each coordinate. Equal total budget forces equality. -/
theorem unique (t : Rat) (rows : List Row)
    (feasible : ∀ r ∈ rows, 0 ≤ r.2.2 ∧ t*r.2.1 ≤ r.1+r.2.2)
    (same : budget (need t) rows = budget (fun r => r.2.2) rows) :
    ∀ r ∈ rows, need t r = r.2.2 := by
  have lower (l : List Row) (h : ∀ r ∈ l, 0 ≤ r.2.2 ∧ t*r.2.1 ≤ r.1+r.2.2) :
      budget (need t) l ≤ budget (fun r => r.2.2) l := by
    induction l with
    | nil => simp [budget]
    | cons x xs ih =>
      have hx := h x (by simp)
      have ht := ih (fun r hr => h r (by simp [hr]))
      have head : need t x ≤ x.2.2 := by unfold need; grind
      simp only [budget]; grind
  induction rows with
  | nil => simp
  | cons x xs ih =>
    have hx := feasible x (by simp)
    have hrest : ∀ r ∈ xs, 0 ≤ r.2.2 ∧ t*r.2.1 ≤ r.1+r.2.2 := fun r hr => feasible r (by simp [hr])
    have h₁ := lower xs hrest
    have h₂ : need t x ≤ x.2.2 := by unfold need; grind
    simp only [budget] at same
    have eq : need t x = x.2.2 := by grind
    have others := ih hrest (by grind)
    intro r mem
    rcases List.mem_cons.mp mem with rfl | mem
    · exact eq
    · exact others r mem
#print axioms unique
end WaterFill
